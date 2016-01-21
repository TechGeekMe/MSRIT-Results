import requests
from bs4 import BeautifulSoup
import re
from results_app.models import Student2, Result2, Subject2
from django.core.exceptions import ObjectDoesNotExist

class FetchedSubject:
    def __init__(self):
        self.course_code = None
        self.subject_name = None
        self.credits_registered = None
        self.credits_earned = None
        self.grade = None
        self.grade_point = None
        self.semester = None
    def __unicode__(self):
        return self.course_code + self.subject_name + str(self.credits_registered)\
               + str(self.credits_earned) + self.grade               
    def __str__(self):          
        return unicode(self).encode('utf-8')
        

class FetchedResult():
    def __init__(self):
        self.usn = None
        self.name = None
        self.department = None
        self.branch_code = None
        self.credits_registered = None
        self.credits_earned = None
        self.sgpa = None
        self.cgpa = None
        self.semester = None
        self.subjects = list()

    def __unicode__(self):
        return self.usn + self.name + self.department + str(self.credits_registered)\
               + str(self.credits_earned) + str(self.sgpa) + str(self.cgpa) + str(self.semester)
               
    def __str__(self):        
        return unicode(self).encode('utf-8')
        


def fetch_result(usn):
    try:
        s = Student2.objects.using('jan2015').get(usn=usn)
    except ObjectDoesNotExist:
        return None
    fr = FetchedResult()
    fr.usn = usn
    fr.department = s.department
    fr.name = s.name
    fr.branch_code = usn[5:7] if usn[5:7] != 'EI' else 'IT'

    r = s.result2
    fr.credits_registered = r.credits_registered
    fr.credits_earned = r.credits_earned
    fr.sgpa = r.sgpa
    fr.cgpa = r.cgpa

    subject_sem = {}
    
    for s in r.subject2_set.all():
        fs = FetchedSubject()
        fs.course_code = s.course_code
        fs.subject_name = s.subject_name
        fs.credits_registered = s.credits_registered
        fs.credits_earned = s.credits_earned
        fs.grade = s.grade
        
        sem = int(re.match(r'[A-Z]+\d', fs.course_code).group()[-1])
        subject_sem[sem] = subject_sem.get(sem, 0) + 1
        fs.semester = sem;
        
        if fs.grade == 'S':
            fs.grade_point = 10
        elif fs.grade == 'A':
            fs.grade_point = 9
        elif fs.grade == 'B':
            fs.grade_point = 8
        elif fs.grade == 'C':
            fs.grade_point = 7
        elif fs.grade == 'D':
            fs.grade_point = 5
        elif fs.grade == 'E':
            fs.grade_point = 4
        else:
            fs.grade_point = 0

        fr.subjects.append(fs)

    fr.semester = max(subject_sem, key=subject_sem.get)

    return fr 
