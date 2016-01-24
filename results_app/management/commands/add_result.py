from . import result_fetcher
from results_app.models import Student, Result, Subject, SubjectList
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import re

def add_usn(usn):
    try:
        s = Student.objects.get(usn=usn)
        if not Result.objects.filter(student=s, date=date(settings.TERM_YEAR, settings.TERM_MONTH, 1)).exists():
            r = result_fetcher.fetch_result(usn)
            # Check if the USN is non-existent for that term
            if r is None:
                raise ValueError("USN %s" % usn)
            put_result(s, r)
            
    except ObjectDoesNotExist:
        r = result_fetcher.fetch_result(usn)
        # Check if the USN is non-existent
        if r is None:
            raise ValueError("USN %s" % usn)
        s = Student(usn=r.usn, name=r.name, department=r.department, branch_code=r.branch_code)
        s.save()
        put_result(s, r)

def put_result(s, r):
        result = Result(student=s, credits_registered=r.credits_registered, credits_earned=r.credits_earned, sgpa=r.sgpa, cgpa=r.cgpa, semester=r.semester, date=date(settings.TERM_YEAR, settings.TERM_MONTH, 1))
        result.save()
        
        for sub in r.subjects:
            subject = Subject(result=result, course_code=sub.course_code, subject_name=sub.subject_name,
                            credits_registered=sub.credits_registered,
                            credits_earned=sub.credits_earned, grade=sub.grade, grade_point=sub.grade_point)
            subject.save()
            if not SubjectList.objects.filter(pk=sub.course_code).exists():
                subjectlist = SubjectList(course_code = sub.course_code,
                                          subject_name=sub.subject_name, department_code=sub.course_code[:2], first_year=True if sub.semester <= 2 and not re.match(r'^[A-Z][A-Z]+E', sub.course_code) else False)
                subjectlist.save()
    
