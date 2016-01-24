from django.contrib import admin

from .models import Student, Result, Subject, SubjectList
    
class ResultInline(admin.StackedInline):
    model = Result

class SubjectInline(admin.StackedInline):
    model = Subject
    
class StudentAdmin(admin.ModelAdmin):
    list_display = ('usn', 'name', 'department')
    inlines = [ResultInline]
    search_fields = ['name', 'usn']

class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'name', 'sgpa', 'cgpa', 'semester')
    inlines = [SubjectInline]
    search_fields = ['student__usn']
    def name(self, obj):
        return obj.student.name
    
class SubjectListAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'subject_name', 'department_code', 'first_year')
    search_fields = ['course_code']

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('usn', 'course_code', 'subject_name')
    search_fields = ['course_code']
    def usn(self, obj):
        return obj.result.student.usn
    
admin.site.register(Student, StudentAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(SubjectList, SubjectListAdmin)
