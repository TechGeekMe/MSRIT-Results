from django.shortcuts import get_object_or_404, render

from django.http import HttpResponseRedirect, HttpResponse

from django.core.urlresolvers import reverse

from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings

from .models import Student, Result, Subject, SubjectList

from datetime import date

from . import add_result

def index(request):
    check_cookie(request);
    return render(request, 'results_app/index.html', {'test': request.session['term']})

def update_db(request, usn_base, first_usn, last_usn):
    bad_usns = 0
    first_usn = int(first_usn)
    last_usn = int(last_usn)
    for i in range(first_usn, last_usn):
        if bad_usns > 5:
            return HttpResponse("Over! Stopped at " + str(usn))
        usn = usn_base + str(i).zfill(3)
        # Check if USN already exists
        if Student.objects.filter(usn=usn).exists():
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
    branches = ['CS', 'IS', 'IT', 'IM', 'EC', 'CV', 'ME', 'TE', 'CH', 'BT', 'EE', 'ML', 'EI', 'AT']
    for branch in branches:
        update_db(request, '1MS'+year+branch, 0, 300)

def pull_dip(request, year):
    branches = ['CS', 'IS', 'IT', 'IM', 'EC', 'CV', 'ME', 'TE', 'CH', 'BT', 'EE', 'ML', 'EI', 'AT']
    for branch in branches:
        update_db(request, '1MS'+year+branch, 400, 500)
        
    return HttpResponse("Success!")


def student_result(request, usn):
    check_cookie(request)
    try:
        student = Student.objects.get(pk=usn)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('results_app:student_not_found'))
    try:
        result = student.result_set.get(date=date(request.session['term']['year'], request.session['term']['month'], 1))
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('results_app:result_not_found'))
    
    subjects = result.subject_set.all()
    return render(request, 'results_app/student_result.html', {'student': student, 'result': result, 'subjects': subjects})

def usn_search(request):
    check_cookie(request)
    usn = '1MS' + request.POST['usn'].upper()
    return HttpResponseRedirect(reverse('results_app:student_result', args=(usn, ))) 
    
def student_name_list(request):
    check_cookie(request)
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

def result_not_found(request):
    return render(request, 'results_app/result_not_found.html')

def get_sem_results(request):
    sem = request.GET['semester']
    branch = request.GET['branch']
    return HttpResponseRedirect(reverse('results_app:sem_results', args=(sem, branch)))

def sem_results(request, sem, branch):
    check_cookie(request)
    results = Result.objects.filter(student__branch_code=branch, semester=sem, date=date(request.session['term']['year'], request.session['term']['month'], 1))
    if results.count() == 0:
        return HttpResponseRedirect(reverse('results_app:student_not_found'))                              
    sort = request.POST.get('sort', 'sgpa')
    if sort == 'name':
        results = results.order_by('student__name')
    elif sort == 'sgpa':
        results = results.order_by('-sgpa')
    elif sort == 'cgpa':
        results = results.order_by('-cgpa')
    return render(request, 'results_app/sem_results.html', {'results': results, 'semester': sem, 'branch': branch, 'branch_name': results[0].student.department, 'sort': sort})
 
def get_subjects(request):
    department = request.POST['department']
    if department == 'FY':
        subjects = SubjectList.objects.filter(first_year=True)
    else:
        subjects = SubjectList.objects.filter(department_code=department, first_year=False)
    resp = ''
    for subject in subjects:
        resp += "<option value=\"%s\">%s %s</option>"% (subject.course_code, subject.course_code, subject.subject_name)
    return HttpResponse(resp)

def get_subject_results(request):
    course_code = request.GET['course_code']
    fybranch = request.GET['fybranch']
    if fybranch == 'NO':
        return HttpResponseRedirect(reverse('results_app:subject_results', args=(course_code, )))
    else:
        return HttpResponseRedirect(reverse('results_app:subject_results_fy', args=(course_code, fybranch)))
    
def subject_results(request, course_code, fybranch='NO'):
    check_cookie(request)
    sort = request.POST.get('sort', 'grade')
    if fybranch == 'NO':
        subjects = Subject.objects.filter(course_code=course_code, result__date=date(request.session['term']['year'], request.session['term']['month'], 1))
    else:
        subjects = Subject.objects.filter(course_code=course_code, result__student__branch_code=fybranch, result__date=date(request.session['term']['year'], request.session['term']['month'], 1))       
    if subjects.count() == 0:
        return HttpResponseRedirect(reverse('results_app:student_not_found'))
    
    if sort == 'name':
        subjects = subjects.order_by('result__student__name')
    else:
        subjects = subjects.order_by('-grade_point')

    dic = {'course_code': course_code, 'subject_name': subjects[0].subject_name, 'subjects': subjects, 'sort': sort, 'fybranch': fybranch}
        
    return render(request, 'results_app/subject_results.html', dic)

def custom_404(request):
    return render(request, 'results_app/404.html')

def custom_500(request):
    return render(request, 'results_app/404.html')

def disclaimer(request):
    return render(request, 'results_app/disclaimer.html')

def check_cookie(request):
    if 'term' not in request.session:
        request.session['term'] = {'month': settings.TERM_MONTH, 'year': settings.TERM_YEAR}
    if 'term' in request.POST:
        term = {'month': int(request.POST['term'][0:2]), 'year': int(request.POST['term'][3:7])}
        request.session['term'] = term
    
    
    
    
