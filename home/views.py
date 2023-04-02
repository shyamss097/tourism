from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from .models import *
from django.contrib.auth.decorators import login_required

def homepage(request):
    return render(request, 'base.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_manager = form.cleaned_data['is_manager']
            user.save()
            # authenticate and log in the user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            # redirect to appropriate dashboard
            if user.is_manager:
                return redirect('home')
            else:
                return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request,'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') # Replace 'home' with your desired redirect URL
        else:
            # Show an error message if authentication fails
            error_message = "Invalid login credentials. Please try again."
            return render(request, 'registration/login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

