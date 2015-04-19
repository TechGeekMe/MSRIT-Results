from django.db import models

class Student(models.Model):
    usn = models.CharField(max_length=15)
    name = models.CharField(max_length=50)
    department= models.CharField(max_length=50)
    def __unicode__(self):
        return self.usn
        

class Result(models.Model):
    student = models.OneToOneField(Student, primary_key=True)
    credits_registered = models.IntegerField()
    credits_earned = models.IntegerField()
    sgpa = models.CharField(max_length=5)
    cgpa = models.CharField(max_length=5)
    def __unicode__(self):
        return str(self.sgpa)

class Subject(models.Model):
    result = models.ForeignKey(Result)
    course_code = models.CharField(max_length=15)
    subject_name = models.CharField(max_length=50)
    credits_registered = models.IntegerField()
    credits_earned = models.IntegerField()
    grade = models.CharField(max_length=5)
    def __unicode__(self):
        return self.subject_name
