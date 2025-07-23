from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import StudentProfile, Program

class StudentRegistrationForm(UserCreationForm):
    program = forms.ModelChoiceField(queryset=Program.objects.all())
    year_of_study = forms.ChoiceField(choices=[(1, 'Year 1'), (2, 'Year 2'), (3, 'Year 3')])
    semester = forms.ChoiceField(choices=[(1, 'Semester 1'), (2, 'Semester 2'), 
                                        (3, 'Semester 3'), (4, 'Semester 4'),
                                        (5, 'Semester 5'), (6, 'Semester 6')])
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'program', 'year_of_study', 'semester']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['program', 'year_of_study', 'semester']