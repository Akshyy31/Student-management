from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,user_passes_test

from django.http import HttpResponseForbidden
from .forms import (
    StudentRegistrationForm,
    StudentFullProfileForm,
    AdminAddStudentForm,
    CourseForm,
    EnrollmentForm,StudentEditForm
)
from .models import CustomUser, Course, Enrollment


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

    enrollments = Enrollment.objects.filter(student=user).select_related("course")

    # Stats
    total_courses = enrollments.count()
    completed_courses = enrollments.filter(status="completed").count()
    active_courses = enrollments.filter(status="active").count()

    # Courses student has NOT enrolled in
    enrolled_ids = enrollments.values_list("course_id", flat=True)
    available_courses = Course.objects.exclude(id__in=enrolled_ids)

    context = {
        "user": user,
        "department_name": department_name,
        "enrollments": enrollments,
        "total_courses": total_courses,
        "completed_courses": completed_courses,
        "active_courses": active_courses,
        "available_courses": available_courses,
    }
    return render(request, "student_dashboard.html", context)


# Admin Dashboard
@login_required
def admin_dashboard(request):
    if request.user.role != "admin":
        return HttpResponseForbidden("Only admins allowed here")

    # Get all students
    students = CustomUser.objects.filter(role="student").select_related("department")

    # Get all enrollments with related student and course
    enrollments = Enrollment.objects.select_related("student", "course").all()

    # Optional: Prepare a summary dictionary for stats
    total_students = students.count()
    total_courses = Course.objects.count()
    total_enrollments = enrollments.count()
    completed_enrollments = enrollments.filter(status="completed").count()
    active_enrollments = enrollments.filter(status="active").count()
    dropped_enrollments = enrollments.filter(status="dropped").count()

    context = {
        "students": students,
        "enrollments": enrollments,
        "total_students": total_students,
        "total_courses": total_courses,
        "total_enrollments": total_enrollments,
        "completed_enrollments": completed_enrollments,
        "active_enrollments": active_enrollments,
        "dropped_enrollments": dropped_enrollments,
    }
    return render(request, "admin_dashboard.html", context)


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

    return render(request, "add_student.html", {"form": form, "title": "Add Student"})


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


@login_required
def edit_course(request, pk):
    if request.user.role != "admin":
        return HttpResponseForbidden()
    course = get_object_or_404(Course, pk=pk)

    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect("course_list")
    else:
        form = CourseForm(instance=course)

    return render(request, "edit_course.html", {"form": form, "course": course})

@login_required
def delete_course(request, pk):
    if request.user.role != "admin":
        return HttpResponseForbidden()
    course = get_object_or_404(Course, pk=pk)

    if request.method == "POST":
        course.delete()
        return redirect("course_list")

    return render(request, "confirm_delete_course.html", {"course": course})


# -------------------------------------------------------------------------------------------------------------------



def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

@login_required
@user_passes_test(is_admin)
def assign_course(request):
    if request.method == "POST":
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect("enrollment_list")
            except:
                form.add_error(None, "This student is already assigned to this course.")
    else:
        form = EnrollmentForm()
    return render(request, "assign_course.html", {"form": form})

@login_required
@user_passes_test(is_admin)
def enrollment_list(request):
    enrollments = Enrollment.objects.select_related("student", "course")
    return render(request, "enrollment_list.html", {"enrollments": enrollments})


@login_required
def add_enrollment(request):
    if request.user.role != "admin":
        return HttpResponseForbidden()
    if request.method == "POST":
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("enrollment_list")
    else:
        form = EnrollmentForm()
    return render(request, "add_enrollment.html", {"form": form})


@login_required
def available_courses(request):
    if request.user.role != "student":
        return HttpResponseForbidden("Only students allowed here")

    user = request.user

    # All courses that the student is NOT already enrolled in
    enrolled_course_ids = user.enrollments.values_list("course_id", flat=True)
    courses = Course.objects.exclude(id__in=enrolled_course_ids)

    context = {"courses": courses}
    return render(request, "available_courses.html", context)


@login_required
def enroll_course(request, course_id):
    if request.user.role != "student":
        return HttpResponseForbidden("Only students allowed here")

    user = request.user
    course = Course.objects.get(id=course_id)

    # Check if already enrolled
    if Enrollment.objects.filter(student=user, course=course).exists():
        return redirect("student_dashboard")  # or show message

    # Create enrollment
    Enrollment.objects.create(student=user, course=course, status="active")
    return redirect("student_dashboard")


@login_required
def student_detail(request, pk):
    if request.user.role != "admin":
        return HttpResponseForbidden("Only admins can view this page")

    student = CustomUser.objects.get(pk=pk, role="student")
    return render(request, "student_detail.html", {"student": student})


def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

@login_required
@user_passes_test(is_admin)
def edit_student(request, student_id):
    student = get_object_or_404(CustomUser, id=student_id, role='student')
    if request.method == "POST":
        form = StudentEditForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect("student_list")  # redirect to student list page
    else:
        form = StudentEditForm(instance=student)
    return render(request, "edit_student.html", {"form": form, "student": student})

def is_admin(user):
    return user.is_authenticated and user.role == 'student'

@login_required
@user_passes_test(is_admin)
def update_enrollment_status(request, enrollment_id, status):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    if status in dict(Enrollment.STATUS_CHOICES).keys():
        enrollment.status = status
        enrollment.save()
    return redirect('student_dashboard')