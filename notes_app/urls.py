# notes_app/urls.py
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('notes/', login_required(views.notes_view), name='notes'),
    path('profile/', views.update_profile, name='update_profile'),
    path('register/success/', views.registration_success, name='registration_success'),
    path('logout/', views.custom_logout, name='logout'),
]