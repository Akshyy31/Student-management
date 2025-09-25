from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate
from student_app import views

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    return render(request, 'profile.html')

def HomeView(request):
    return render(request, 'base.html')