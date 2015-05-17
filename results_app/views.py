from django.shortcuts import render

from django.http import HttpResponse

from .models import Student, Result, Subject

from . import result_fetcher

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
            r = result_fetcher.fetch_result(usn)
            # Check if the USN is non-existent
                
            if r is None:
                raise ValueError("USN %s" % usn)

            s = Student(usn=r.usn, name=r.name, department=r.department)
            s.save()
            result = Result(student=s, credits_registered=r.credits_registered, credits_earned=r.credits_earned, sgpa=r.sgpa, cgpa=r.cgpa)
            result.save()
            
            for sub in r.subjects:
                subject = Subject(result=result, course_code=sub.course_code, subject_name=sub.subject_name,
                                credits_registered=sub.credits_registered,
                                credits_earned=sub.credits_earned, grade=sub.grade)
                subject.save()

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
        

def test(request):
    s = Student(usn='1msdummy', name='dummy', department='dummydep')
    s.save()
    return HttpResponse('Test Done!')
    
