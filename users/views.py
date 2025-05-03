from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import RegistrationForm, LoginForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required


@csrf_protect
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Altere para sua view de home
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    return render(request, 'users/home.html')