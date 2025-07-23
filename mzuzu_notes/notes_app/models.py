from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Program(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return f"{self.code} - {self.name}"

class Semester(models.Model):
    name = models.CharField(max_length=50, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)
    
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return self.name
    
    def clean(self):
        if self.end_date <= self.start_date:
            raise ValidationError("End date must be after start date")
        
    def save(self, *args, **kwargs):
        if self.is_current:
            # Ensure only one semester is marked as current
            Semester.objects.exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True)
    semester = models.CharField(max_length=50)
    year_of_study = models.IntegerField(choices=[(1, 'Year 1'), (2, 'Year 2'), (3, 'Year 3')], default=1)
    current_semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True)
    is_approved = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Student Profile"
        verbose_name_plural = "Student Profiles"
        permissions = [
            ("can_approve", "Can approve student profiles"),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.get_status_display()}"
    
    def get_status_display(self):
        if self.is_approved:
            return f"Approved ({self.program})" if self.program else "Approved"
        return "Pending Approval"

class Course(models.Model):
    programs = models.ManyToManyField(Program, related_name='courses')
    semester = models.ForeignKey(
        Semester,
        on_delete=models.CASCADE,
        related_name='courses',
        null=False  # This will be non-nullable after we migrate
    )
    year = models.IntegerField(
        choices=[(1, 'Year 1'), (2, 'Year 2'), (3, 'Year 3')]
    )
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    credits = models.PositiveIntegerField(default=3)

    class Meta:
        ordering = ['code']
        unique_together = ['code', 'semester']  # Ensure course code is unique per semester

    def __str__(self):
        return f"{self.code} - {self.name} ({self.semester.name})"

class Note(models.Model):
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE,
        related_name='notes'
    )
    title = models.CharField(max_length=200)
    pdf_file = models.FileField(upload_to='notes/pdfs/%Y/%m/%d/')
    extracted_text = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='uploaded_notes'
    )
    
    class Meta:
        ordering = ['title']  # Changed from upload_date to title
    
    def __str__(self):
        return f"{self.title} ({self.course.code})"
    
    def save(self, *args, **kwargs):
        # Set uploader if not specified
        if not self.uploaded_by_id and hasattr(self, 'request'):
            self.uploaded_by = self.request.user
        
        super().save(*args, **kwargs)
        
        # Extract text if not already done
        if not self.extracted_text:
            self.extract_text_from_pdf()
    
    def extract_text_from_pdf(self):
        """Extract text content from PDF file"""
        import PyPDF2
        text = ""
        try:
            with self.pdf_file.open('rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
                self.extracted_text = text
                # Save the extracted text
                Note.objects.filter(pk=self.pk).update(extracted_text=text)
        except Exception as e:
            print(f"Error extracting text: {e}")