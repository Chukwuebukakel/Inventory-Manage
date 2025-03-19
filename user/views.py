from django.shortcuts import render, redirect

from .forms import CreateUserForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from user.forms import User



# Create your views here.

def registerView(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account has been created for {username}. Continue to Login')
            return redirect('dashboard-login')
    else:    
        form = CreateUserForm()

    context = {
        'form':form
    }
    return render(request, 'register.html', context)



def loginView(request):
    if request.user.is_authenticated:
        return redirect("dashboard-index")  # Redirect if already logged in

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("dashboard-index")  # Redirect after successful login
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("dashboard.register")

    return render(request, "login.html")  # Render the login template



def logoutView(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect("dashboard-login")  # Redirect to login page after logout


def profile(request):
    return render(request, 'profile.html') # Render the profile template

def profile_update(request):
    if request.method=='POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('dashboard-profile')
    else:
        user_form = UserUpdateForm(instance=request.user) 
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'profile_update.html', context)



