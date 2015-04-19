from django.shortcuts import render

from django.http import HttpResponse

from .models import Student, Result, Subject

from . import add_result

import global_vars

nonexistent_usns = 0

def index(request):
    return HttpResponse("Hi")

def update_db(request):
    global_vars.init()
    usn_base = "1MS13CH"
    for i in range(1, 144):
        if global_vars.bad_usns > 5:
            return HttpResponse("Over!")
        usn = usn_base + str(i).zfill(3)
        # Check if USN already exists
        if Student.objects.filter(usn=usn):
            continue
        add_result.add_usn(usn)
    return HttpResponse("Done!")

def clean_db(request):
    usn_base = "1ms13is"
    for i in range(1, 138):
        usn = usn_base + str(i).zfill(3)
        Student.objects.filter(usn=usn).delete()
        
    
    
