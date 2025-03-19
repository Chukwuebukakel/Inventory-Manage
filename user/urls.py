from django.urls import path

from user import views

app_name = "user"

urlpatterns = [
    path("register/", views.registerView, name="dashboard-register"),
    path('login/', views.loginView, name='dashboard-login'),
    path('logout/', views.logoutView, name='dashboard-logout'),
]