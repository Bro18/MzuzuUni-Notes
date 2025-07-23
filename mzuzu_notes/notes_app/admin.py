from django.contrib import admin
from .models import Program, Course, Note, StudentProfile, Semester
from django.utils import timezone
from datetime import timedelta

class CourseProgramInline(admin.TabularInline):
    model = Course.programs.through
    extra = 1

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    inlines = [CourseProgramInline]
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    filter_horizontal = ('programs',)
    list_display = ('code', 'name', 'year', 'semester')
    list_filter = ('year', 'semester', 'programs')
    search_fields = ('code', 'name')
    
    def get_changeform_initial_data(self, request):
        return {'semester': Semester.objects.filter(is_current=True).first()}

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'uploaded_by')
    list_filter = ('course__programs', 'course__year')
    search_fields = ('title', 'course__name', 'extracted_text')

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'program', 'year_of_study', 'current_semester')
    list_filter = ('program', 'year_of_study', 'current_semester')
    search_fields = ('user__username',)

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_current', 'duration_days')
    list_editable = ('is_current',)
    search_fields = ('name',)
    date_hierarchy = 'start_date'
    actions = ['make_current_semester']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'is_current')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date'),
            'description': '<strong>Note:</strong> End date must be after start date'
        }),
    )
    
    def duration_days(self, obj):
        return (obj.end_date - obj.start_date).days
    duration_days.short_description = 'Duration (days)'
    
    def make_current_semester(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "Please select exactly one semester", level='error')
            return
        semester = queryset.first()
        semester.is_current = True
        semester.save()
    make_current_semester.short_description = "Mark selected as current semester"