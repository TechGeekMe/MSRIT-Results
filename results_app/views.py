from django.shortcuts import get_object_or_404, render

from django.http import HttpResponseRedirect, HttpResponse

from django.core.urlresolvers import reverse

from .models import Student, Result, Subject, SubjectList

from . import add_result

import requests

from bs4 import BeautifulSoup

from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    return render(request, 'results_app/index.html')

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
    lastSeenUsn = ''
    rows = Student.objects.all().order_by('usn')
    for row in rows:
      if row.usn == lastSeenUsn:
        row.delete() # We've seen this id in a previous row
      else: # New id found, save it and check future rows for duplicates.
        lastSeenUsn = row.usn
        

def pull(request, year):
    branches = ['CS', 'IS', 'IT', 'IM', 'EC', 'CV', 'ME', 'TE', 'CH', 'BT', 'EE', 'ML']
    for branch in branches:
        update_db(request, '1MS'+year+branch, 0, 300)

def pull_dip(request, year):
    branches = ['CS', 'IS', 'IT', 'IM', 'EC', 'CV', 'ME', 'TE', 'CH', 'BT', 'EE', 'ML']
    for branch in branches:
        update_db(request, '1MS'+year+branch, 400, 500)
        
    return HttpResponse("Success!")


def student_result(request, usn):
    student = get_object_or_404(Student, pk=usn)
    result = student.result_set.all()[0]
    subjects = result.subject_set.all()
    
    return render(request, 'results_app/student_result.html', {'student': student, 'result': result, 'subjects': subjects})

def usn_search(request):
    usn = '1MS' + request.POST['usn'].upper()
    return HttpResponseRedirect(reverse('results_app:student_result', args=(usn, ))) 

    
def student_name_list(request):
    #add redirect for no name match found
    name = request.POST['student_name']
    students = Student.objects.filter(name__icontains=name)
    if students.count() == 0:
        return HttpResponseRedirect(reverse('results_app:student_not_found'))
    elif students.count() == 1:
        return HttpResponseRedirect(reverse('results_app:student_result', args=(students[0].usn,)))
    else:
        return render(request, 'results_app/student_name_list.html', {'name': name, 'students': students}) 
        
def student_not_found(request):
    return render(request, 'results_app/student_not_found.html')

def sem_results(request):
    sem = request.POST['semester']
    branch = request.POST['branch']
    results = Result.objects.filter(student__branch_code=branch, semester=sem)
    sort = request.POST['sort']
    if sort == 'name':
        results = results.order_by('student__name')
    elif sort == 'sgpa':
        results = results.order_by('-sgpa')
    elif sort == 'cgpa':
        results = results.order_by('-cgpa')
    return render(request, 'results_app/sem_results.html', {'results': results, 'semester': sem, 'branch': branch, 'branch_name': results[0].student.department, 'sort': sort})

def get_subjects(request):
    branch = request.POST['branch']
    subjects = SubjectList.objects.filter(branch_code=branch)
    resp = ''
    for subject in subjects:
        resp += "<option value=\"%s\">%s</option>"% (subject.course_code, subject.subject_name)
    return HttpResponse(resp)

def subject_results(request):
    course_code = request.POST['course_code']
    sort = request.POST['sort']
    subjects = Subject.objects.filter(course_code=course_code)
    if sort == 'name':
        subjects = subjects.order_by('result__student__name')
    if sort == 'grade':
        subjects = subjects.order_by('-grade_point')
    
    return render(request, 'results_app/subject_results.html', {'course_code': course_code, 'subject_name': subjects[0].subject_name, 'subjects': subjects, 'sort': sort})

def custom_404(request):
    return render(request, 'results_app/404.html')

def custom_500(request):
    return render(request, 'results_app/404.html')
    
    
    
