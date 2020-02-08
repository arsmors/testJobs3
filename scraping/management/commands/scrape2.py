from django.core.management.base import BaseCommand
from urllib.request import urlopen

from bs4 import BeautifulSoup
import json
from scraping.models import Job
from selenium.webdriver.common.by import By


class Command(BaseCommand):
    help = "collect jobs"

    def handle(self, *args, **options):
        html = urlopen('https://www.cv.lv/darba-sludinajumi/q-automation')
        soup = BeautifulSoup(html, 'html.parser')
        postings = soup.find_all("div", class_="cvo_module_offer")
        for p in postings:
            url = p.find('a', itemprop='title')['href']
            title = p.find(itemprop='title').text

            alga = p.find(class_='salary-blue')
            if alga is not None:
                alga_value = alga.get_text()

            company = p.find(itemprop='hiringOrganization').text

            location = p.find(itemprop='jobLocation')
            if location is not None:
                location_value = location.get_text()

            try:
                Job.objects.create(
                    title=title,
                    alga=alga_value,
                    company=company,
                    location=location_value,
                    url=url
                )
                print('%s added' % (title,))
            except:
                print('%s already exists' % (title,))
        self.stdout.write( 'job complete' )
