from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import StudentRegistrationForm, StudentFullProfileForm,AdminAddStudentForm,CourseForm
from .models import CustomUser,Course


# Home
def HomeView(request):
    return render(request, "base.html")


# Registration
def register(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # just save the CustomUser
            return redirect("login")
    else:
        form = StudentRegistrationForm()
    return render(request, "register.html", {"form": form})


# Login
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect based on role
            if user.role == "admin":
                return redirect("admin_dashboard")
            else:
                return redirect("student_dashboard")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")


# Logout
def logout_view(request):
    logout(request)
    return redirect("login")


# User Profile
@login_required
def profile_view(request):
    user = request.user
    context = {"user": user}
    return render(request, "profile.html", context)


# Edit Profile
@login_required
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        form = StudentFullProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("student_dashboard")
    else:
        form = StudentFullProfileForm(instance=user)
    return render(request, "edit_profile.html", {"form": form})


# Student Dashboard
@login_required
def student_dashboard(request):
    if request.user.role != "student":
        return HttpResponseForbidden("Only students allowed here")

    user = request.user
    department_name = user.department.name if user.department else "Not Assigned"
    context = {
        "user": user,
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
def student_list(request):
    if request.user.role != "admin":
        return HttpResponseForbidden("Only admins can manage students.")

    students = CustomUser.objects.filter(role="student")
    context = {"students": students}
    return render(request, "student_list.html", context)


@login_required
def admin_add_student(request):
    if request.user.role != "admin":
        return HttpResponseForbidden("Only admins can manage students.")

    if request.method == "POST":
        form = AdminAddStudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.role = "student"
            student.save()
            return redirect("student_list")
    else:
        form = AdminAddStudentForm()

    return render(
        request, "add_student.html", {"form": form, "title": "Add Student"}
    )

@login_required
def course_list(request):
    if request.user.role != "admin":
        return HttpResponseForbidden()
    courses = Course.objects.all()
    return render(request, "courses.html", {"courses": courses})

@login_required
def add_course(request):
    if request.user.role != "admin":
        return HttpResponseForbidden()
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("course_list")
    else:
        form = CourseForm()
    return render(request, "add_course.html", {"form": form})