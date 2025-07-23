# notes_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('notes/', views.notes_view, name='notes'),
    path('profile/', views.update_profile, name='update_profile'),
]