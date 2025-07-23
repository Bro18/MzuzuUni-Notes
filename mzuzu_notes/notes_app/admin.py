# notes_app/admin.py
from django.contrib import admin
from .models import Program, Course, Note, StudentProfile

class CourseInline(admin.TabularInline):
    model = Course
    extra = 1

class ProgramAdmin(admin.ModelAdmin):
    inlines = [CourseInline]

class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'upload_date')
    list_filter = ('course__program', 'course__year', 'course__semester')
    search_fields = ('title', 'course__name', 'extracted_text')

admin.site.register(Program, ProgramAdmin)
admin.site.register(Course)
admin.site.register(Note, NoteAdmin)
admin.site.register(StudentProfile)