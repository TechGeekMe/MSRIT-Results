from django.contrib import admin

from .models import Student,Result,Subject

class StudentInline(admin.StackedInline):
    model = Result
    
class ResultInline(admin.StackedInline):
    model = Result

class SubjectInline(admin.StackedInline):
    model = Subject
    
class StudentAdmin(admin.ModelAdmin):
    list_display = ('usn', 'name', 'department')
    inlines = [ResultInline]

class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'name', 'sgpa', 'cgpa')
    inlines = [SubjectInline]
    def name(self, obj):
        return obj.student.name

admin.site.register(Student,StudentAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Subject)
