from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import StudentRegistrationForm,StudentFullProfileForm
from .models import CustomUser, StudentProfile, Department


def HomeView(request):
    return render(request, "base.html")


# Registration
def register(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  
    else:
        form = StudentRegistrationForm()
    return render(request, "register.html", {"form": form})


# Login
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # redirect based on role
            if user.role == "admin":
                return redirect("admin_dashboard")
            else:
                return redirect("student_dashboard")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")


# user profile
@login_required
def profile_view(request):
    profile = get_object_or_404(StudentProfile, user=request.user)
    context = {"profile": profile}
    return render(request, "profile.html", context)


# Logout
def logout_view(request):
    logout(request)
    return redirect("login")


# Student Dashboard
@login_required
def student_dashboard(request):
    if request.user.role != "student":
        return HttpResponseForbidden("Only students allowed here")

    # get the student's profile (1-to-1 with CustomUser)
    profile = get_object_or_404(StudentProfile, user=request.user)
    department_name = profile.department.name if profile.department else "Not Assigned"
    context = {
        "profile": profile,
        "department_name": department_name,
    }
    return render(request, "student_dashboard.html", context)


# Admin Dashboard
@login_required
def admin_dashboard(request):
    if request.user.role != "admin":
        return HttpResponseForbidden("Only admins allowed here")
    return render(request, "admin_dashboard.html")


@login_required
def edit_profile(request):
    profile = get_object_or_404(StudentProfile, user=request.user)

    if request.method == "POST":
        form = StudentFullProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("student_dashboard")
    else:
        form = StudentFullProfileForm(instance=profile, user=request.user)

    return render(request, "edit_profile.html", {"form": form})