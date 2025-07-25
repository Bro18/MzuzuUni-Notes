# mzuzu_notes/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.decorators.cache import never_cache
from notes_app import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('notes_app.urls')),
    
    # Secure logout using Django's built-in LogoutView
    path('logout/', 
        never_cache(auth_views.LogoutView.as_view(
            template_name='logout_confirmation.html',
            next_page='home'  # Redirect to home after logout
        )),
        name='logout'  # Note: We're using 'logout' as the name now
    ),
    
    path('login/', 
        auth_views.LoginView.as_view(
            template_name='login.html'
        ), 
        name='login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)