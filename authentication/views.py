from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, WorkerProfileForm, EmployerProfileForm, LoginForm
from .models import User, WorkerProfile, EmployerProfile

def register_view(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            username = user_form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            
            # Create profile based on role
            if user.role == 'worker':
                return redirect('authentication:complete_worker_profile')
            elif user.role == 'employer':
                return redirect('authentication:complete_employer_profile')
            else:
                return redirect('authentication:login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = CustomUserCreationForm()
    
    return render(request, 'authentication/register.html', {'user_form': user_form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                
                # Redirect based on role
                if user.role == 'admin':
                    return redirect('hiring:admin_dashboard')
                elif user.role == 'worker':
                    return redirect('workers:worker_dashboard')
                elif user.role == 'employer':
                    return redirect('hiring:employer_dashboard')
                else:
                    return redirect('authentication:home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LoginForm()
    
    return render(request, 'authentication/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('authentication:login')

@login_required
def complete_worker_profile(request):
    try:
        profile = request.user.worker_profile
    except WorkerProfile.DoesNotExist:
        profile = WorkerProfile(user=request.user)
    
    if request.method == 'POST':
        form = WorkerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your worker profile has been completed!')
            return redirect('workers:worker_dashboard')
    else:
        form = WorkerProfileForm(instance=profile)
    
    return render(request, 'authentication/complete_worker_profile.html', {'form': form})

@login_required
def complete_employer_profile(request):
    try:
        profile = request.user.employer_profile
    except EmployerProfile.DoesNotExist:
        profile = EmployerProfile(user=request.user)
    
    if request.method == 'POST':
        form = EmployerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your employer profile has been completed!')
            return redirect('hiring:employer_dashboard')
    else:
        form = EmployerProfileForm(instance=profile)
    
    return render(request, 'authentication/complete_employer_profile.html', {'form': form})

def home_view(request):
    if request.user.is_authenticated:
        if request.user.role == 'admin':
            return redirect('hiring:admin_dashboard')
        elif request.user.role == 'worker':
            return redirect('workers:worker_dashboard')
        elif request.user.role == 'employer':
            return redirect('hiring:employer_dashboard')
    
    return render(request, 'home.html')
