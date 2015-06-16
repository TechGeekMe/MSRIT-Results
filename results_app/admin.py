from django.contrib import admin

from .models import Student,Result,Subject
    
class ResultInline(admin.StackedInline):
    model = Result

class SubjectInline(admin.StackedInline):
    model = Subject
    
class StudentAdmin(admin.ModelAdmin):
    list_display = ('usn', 'name', 'department')
    inlines = [ResultInline]
    search_fields = ['name']

class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'name', 'sgpa', 'cgpa', 'semester')
    inlines = [SubjectInline]
    search_fields = ['student__usn']
    def name(self, obj):
        return obj.student.name

admin.site.register(Student,StudentAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Subject)
