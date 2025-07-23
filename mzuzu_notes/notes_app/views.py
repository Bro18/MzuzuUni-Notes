from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import StudentRegistrationForm, ProfileUpdateForm
from .models import Program, StudentProfile, Course, Note
from django.contrib import messages

def home(request):
    if request.user.is_authenticated:
        return redirect('notes')
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create student profile
            program = form.cleaned_data.get('program')
            year_of_study = form.cleaned_data.get('year_of_study')
            semester = form.cleaned_data.get('semester')
            
            StudentProfile.objects.create(
                user=user,
                program=program,
                year_of_study=year_of_study,
                semester=semester
            )
            
            login(request, user)
            return redirect('notes')
    else:
        form = StudentRegistrationForm()
    return render(request, 'register.html', {'form': form})

def notes_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        profile = request.user.studentprofile
    except StudentProfile.DoesNotExist:
        # Redirect to profile update with message
        messages.warning(request, 'Please complete your profile first')
        return redirect('update_profile')
    
    # Check if profile is complete
    if not all([profile.program, profile.year_of_study, profile.semester]):
        messages.warning(request, 'Please complete your profile details')
        return redirect('update_profile')
    
    notes = Note.objects.filter(
        course__program=profile.program,
        course__year=profile.year_of_study,
        course__semester=profile.semester
    )
    
    return render(request, 'notes.html', {
        'notes': notes,
        'profile': profile
    })

def update_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        profile = request.user.studentprofile
    except StudentProfile.DoesNotExist:
        profile = StudentProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('notes')
    else:
        form = ProfileUpdateForm(instance=profile)
    
    return render(request, 'profile.html', {'form': form})