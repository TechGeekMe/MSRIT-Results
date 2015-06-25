from . import result_fetcher

from .models import Student, Result, Subject, SubjectList

def add_usn(usn):
    
    r = result_fetcher.fetch_result(usn)
    
    # Check if the USN is non-existent
    if r is None:
        raise ValueError("USN %s" % usn)

    s = Student(usn=r.usn, name=r.name, department=r.department, branch_code=r.branch_code)
    s.save()
    result = Result(student=s, credits_registered=r.credits_registered, credits_earned=r.credits_earned, sgpa=r.sgpa, cgpa=r.cgpa, semester=r.semester if r.semester <= 8 else 8)
    result.save()
    
    for sub in r.subjects:
        subject = Subject(result=result, course_code=sub.course_code, subject_name=sub.subject_name,
                        credits_registered=sub.credits_registered,
                        credits_earned=sub.credits_earned, grade=sub.grade, grade_point=sub.grade_point)
        subject.save()
        if not SubjectList.objects.filter(pk=sub.course_code).exists():
            subjectlist = SubjectList(course_code = sub.course_code,
                                      subject_name=sub.subject_name, branch_code=sub.course_code[:2])
            subjectlist.save()
