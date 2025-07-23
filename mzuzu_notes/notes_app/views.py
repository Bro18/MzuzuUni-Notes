from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import StudentRegistrationForm, ProfileUpdateForm
from .models import Program, StudentProfile, Course, Note, Semester
from django.contrib import messages
from django.conf import settings
from django.db.models import Prefetch
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from django.contrib.auth import logout

@require_POST  # Only allow POST requests (for security)
def custom_logout(request):
    logout(request)  # Destroy server session
    response = redirect('home')
    response.delete_cookie('sessionid')  # Clear client-side cookie
    return response

def home(request):
    if request.user.is_authenticated:
        try:
            profile = request.user.studentprofile
            if not profile.is_approved:
                messages.warning(request, 'Your account is pending approval')
                return render(request, 'home.html')
            
            current_semester = Semester.objects.filter(is_current=True).first()
            if not current_semester:
                messages.error(request, 'No active semester found')
                return render(request, 'home.html')
            
            if profile.current_semester != current_semester:
                messages.warning(request, 'You do not have access to the current semester')
                return render(request, 'home.html')
            
            # Get courses with their notes
            courses = Course.objects.filter(
                programs=profile.program,
                year=profile.year_of_study,
                semester=profile.current_semester
            ).prefetch_related(
                Prefetch('notes', queryset=Note.objects.order_by('title'))
            ).order_by('name')
            
            course_notes = [
                {
                    'course': course,
                    'notes': course.notes.all()
                } 
                for course in courses 
                if course.notes.exists()
            ]
            
            context = {
                'course_notes': course_notes,
                'profile': profile,
                'current_semester': current_semester
            }
            return render(request, 'notes.html', context)
        except StudentProfile.DoesNotExist:
            messages.warning(request, 'Please complete your profile')
            return render(request, 'home.html')
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            
            StudentProfile.objects.create(
                user=user,
                program=form.cleaned_data['program'],
                year_of_study=form.cleaned_data['year_of_study'],
                semester=form.cleaned_data['semester'],
                is_approved=False
            )
            
            messages.success(
                request,
                'Thank you for creating an account! '
                'Your registration is under review. '
                'We will get back to you within 24 hours.'
            )
            return redirect('registration_success')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'register.html', {'form': form})

def registration_success(request):
    return render(request, 'registration_success.html')

@login_required(login_url='login') 
def notes_view(request):
    if not request.user.is_authenticated:
        return render(request, 'notes.html')
    
    try:
        profile = request.user.studentprofile
    except StudentProfile.DoesNotExist:
        messages.warning(request, 'Your profile was automatically created with default values')
        profile = StudentProfile.objects.create(
            user=request.user,
            program=Program.objects.first(),
            year_of_study=1,
            current_semester=Semester.objects.filter(is_current=True).first(),
            is_approved=False
        )
        return redirect('home')
    
    if not profile.is_approved:
        messages.warning(request, 'Your account is pending approval')
        return redirect('home')
    
    if not profile.current_semester:
        messages.error(request, 'No semester assigned to your profile')
        return redirect('home')
    
    # Get courses for the student's program, year, and current semester
    courses = Course.objects.filter(
        programs=profile.program,
        year=profile.year_of_study,
        semester=profile.current_semester  # Filter by semester ForeignKey
    ).prefetch_related(
        Prefetch('notes', queryset=Note.objects.order_by('title'))
    ).order_by('code')
    
    course_notes = [
        {
            'course': course,
            'notes': course.notes.all()
        } 
        for course in courses 
        if course.notes.exists()
    ]
    
    context = {
        'course_notes': course_notes,
        'profile': profile,
        'current_semester': profile.current_semester
    }
    return render(request, 'notes.html', context)

def update_profile(request):
    messages.info(request, 'Profile updates are not allowed after registration')
    return redirect('home')

def student_view(request):
    if not request.user.is_authenticated:
        raise PermissionDenied("Please login to access this page")
    
    if not hasattr(request.user, 'studentprofile'):
        raise PermissionDenied("Student profile not found")
    
    if not request.user.studentprofile.is_approved:
        raise PermissionDenied("Your student account hasn't been approved yet.")
    
    return render(request, 'student_dashboard.html')

def logout_confirmation(request):
    return render(request, 'logout_confirmation.html')