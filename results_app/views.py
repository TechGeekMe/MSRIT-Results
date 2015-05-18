from django.shortcuts import render

from django.http import HttpResponse

from .models import Student, Result, Subject

from . import add_result

import requests

from bs4 import BeautifulSoup

nonexistent_usns = 0

def index(request):
    return HttpResponse("Hi")

def update_db(request, usn_base, first_usn, last_usn):
    bad_usns = 0
    first_usn = int(first_usn)
    last_usn = int(last_usn)
    for i in range(first_usn, last_usn):
        if bad_usns > 5:
            return HttpResponse("Over! Stopped at " + str(usn))
        usn = usn_base + str(i).zfill(3)
        # Check if USN already exists
        if Student.objects.filter(usn=usn):
            bad_usns = 0
            continue
        try:
            add_result.add_usn(usn)
            bad_usns = 0
        except ValueError:
            bad_usns += 1

    return HttpResponse("Complete! Stopped at" + str(usn))

def clean_db(request):
    usn_base = "1MS13IS"
    for i in range(1, 138):
        usn = usn_base + str(i).zfill(3)
        Student.objects.filter(usn=usn).delete()
    return HttpResponse("Cleaned")
        

def pull(request, year):
    branches = ['CS', 'IS', 'IT', 'IM', 'EC', 'CV', 'ME', 'TE', 'CH', 'BT', 'EE', 'ML']
    for branch in branches:
        update_db(request, '1MS'+year+branch, 0, 300)
        
    return HttpResponse("Success!")
