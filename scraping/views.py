from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Job


def job_list_view(request):
    queryset = Job.objects.all()
    context = {
        "object_list": queryset
    }
    return render(request, "static.html", context)
