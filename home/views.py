from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import UserSignupForm, ManagerSignupForm, UserLoginForm, ManagerLoginForm
from .models import User, Manager

def homepage(request):
    return render(request, 'base.html')


def user_signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_manager = False
            user.save()
            user_profile = User(user=user, phone=form.cleaned_data['phone'], address=form.cleaned_data['address'])
            user_profile.save()
            login(request, user)
            return redirect('user_dashboard')
    else:
        form = UserSignupForm()
    return render(request, 'user_signup.html', {'form': form})


def manager_signup(request):
    if request.method == 'POST':
        form = ManagerSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_manager = True
            user.save()
            manager_profile = Manager(user=user, phone=form.cleaned_data['phone'])
            manager_profile.save()
            login(request, user)
            return redirect('manager_dashboard')
    else:
        form = ManagerSignupForm()
    return render(request, 'manager_signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_manager is False:
                login(request, user)
                return redirect('user_dashboard')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = UserLoginForm()
    return render(request, 'user_login.html', {'form': form})


def manager_login(request):
    if request.method == 'POST':
        form = ManagerLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_manager is True:
                login(request, user)
                return redirect('manager_dashboard')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = ManagerLoginForm()
    return render(request, 'manager_login.html', {'form': form})
