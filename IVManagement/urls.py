"""
URL configuration for IVManagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from user import views as dashboard_view 
from django.conf import settings 
from django.conf.urls.static import static 
from django.contrib.auth import views as auth_views

# from django.contrib.auth import views as auth_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('register/', dashboard_view.registerView, name='dashboard-register'),
    path('', dashboard_view.loginView, name='dashboard-login'),
    path('logout/', dashboard_view.logoutView, name='dashboard-logout'),
    path('profile/', dashboard_view.profile, name='dashboard-profile'),
    path('profile/update/', dashboard_view.profile_update, name='dashboard-profile_update'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="password_reset_form.html"), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name='password_reset_complete'),


   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 



