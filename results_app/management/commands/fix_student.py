from . import result_fetcher
from results_app.models import Student, Result, Subject, SubjectList
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import re

def fix_usn(usn):
    try:
        s = Student.objects.get(usn=usn)
        r = result_fetcher.fetch_result(usn)
        if r is None:
            raise ValueError("USN %s" % usn)
        dept = r.department
        s.department = dept
        s.save()
        print s.department
    except ObjectDoesNotExist:
        raise ValueError("USN %s" % usn)
    
