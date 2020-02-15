import urllib

from django.core.management.base import BaseCommand
from urllib.request import urlopen

from bs4 import BeautifulSoup

import ssl

ssl._create_default_https_context = ssl._create_unverified_context
import json
from scraping.models import Job
from selenium.webdriver.common.by import By


class Command(BaseCommand):
    help = "collect jobs"

    def handle(self, *args, **options):
        html = urllib.request.urlopen('https://www.likeit.lv/jobs/testing/?category=50')
        soup = BeautifulSoup(html, 'html.parser')
        postings = soup.find_all("div", class_="position-wrapper")
        for p in postings:
            url = p.find('a')['href']
            title = p.find('h4').text
            company = p.find(class_='company')
            if company is not None:
                company = company.get_text()

            try:
                Job.objects.create(
                    title=title,
                    # alga=alga_value,
                    company=company,
                    # location=location_value,
                    url=url
                )
                print('%s added' % (title,))
            except:
                print('%s already exists' % (title,))
        self.stdout.write('job complete')
