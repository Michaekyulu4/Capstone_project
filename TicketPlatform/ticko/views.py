from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()

    # Always return this at the end for both GET and invalid POST
    return render(request, 'ticko/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'ticko/login.html')


@login_required
def dashboard_view(request):
    return render(request, 'ticko/dashboard.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')