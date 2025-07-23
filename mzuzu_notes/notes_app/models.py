# notes_app/models.py
from django.db import models
from django.contrib.auth.models import User  # Import User here (not in apps.py)

class Program(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True)
    year_of_study = models.IntegerField(choices=[(1, 'Year 1'), (2, 'Year 2'), (3, 'Year 3')])
    semester = models.IntegerField(choices=[(1, 'Semester 1'), (2, 'Semester 2'), 
                                          (3, 'Semester 3'), (4, 'Semester 4'),
                                          (5, 'Semester 5'), (6, 'Semester 6')])
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class Course(models.Model):
    programs = models.ManyToManyField(Program)  # Changed from ForeignKey to ManyToMany
    year = models.IntegerField(choices=[(1, 'Year 1'), (2, 'Year 2'), (3, 'Year 3')])
    semester = models.IntegerField(choices=[(1, 'Semester 1'), (2, 'Semester 2'),
                                          (3, 'Semester 3'), (4, 'Semester 4'),
                                          (5, 'Semester 5'), (6, 'Semester 6')])
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.code}: {self.name}"

class Note(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    pdf_file = models.FileField(upload_to='notes/pdfs/')
    extracted_text = models.TextField(blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    @classmethod
    def get_notes_for_student(cls, student_profile):
        return cls.objects.filter(
            course__programs=student_profile.program,
            course__year=student_profile.year_of_study,
            course__semester=student_profile.semester
        ).distinct()
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.extracted_text:
            self.extract_text_from_pdf()
    
    def extract_text_from_pdf(self):
        import PyPDF2
        text = ""
        try:
            pdf_reader = PyPDF2.PdfReader(self.pdf_file)
            for page in pdf_reader.pages:
                text += page.extract_text()
            self.extracted_text = text
            self.save()
        except Exception as e:
            print(f"Error extracting text: {e}")