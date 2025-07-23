# management/commands/update_semesters.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from notes_app.models import Semester, StudentProfile
from datetime import timedelta

class Command(BaseCommand):
    help = 'Updates current semester and student progressions'
    
    def handle(self, *args, **options):
        today = timezone.now().date()
        
        # Check if current semester has ended
        current_semester = Semester.objects.filter(is_current=True).first()
        if current_semester and current_semester.end_date < today:
            # Find next semester
            next_semester = Semester.objects.filter(
                start_date__gt=current_semester.end_date
            ).order_by('start_date').first()
            
            if next_semester:
                # Update students
                students = StudentProfile.objects.filter(
                    current_semester=current_semester,
                    is_approved=True
                )
                
                for student in students:
                    # Check if year should increment
                    if next_semester.name.startswith('Semester 1'):
                        student.year_of_study += 1
                    
                    student.semester = int(next_semester.name.split()[-1])
                    student.current_semester = next_semester
                    student.save()
                
                # Update current semester
                current_semester.is_current = False
                current_semester.save()
                next_semester.is_current = True
                next_semester.save()