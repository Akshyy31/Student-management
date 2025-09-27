from django.contrib.auth.models import AbstractUser
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("student", "Student"),
    )

    # role field
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="student")

    # student-specific fields
    roll_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    department = models.ForeignKey(Department,max_length=100, on_delete=models.SET_NULL,null=True)
    year_of_admission = models.IntegerField(blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


# student_app/models.py

from django.db import models
from django.conf import settings


class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)  # e.g., CS101
    description = models.TextField(blank=True, null=True)
    credits = models.IntegerField(default=3)
    department = models.ForeignKey(
        "Department", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.code} - {self.name}"


class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="enrollments"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="enrollments"
    )
    enrollment_date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[("active", "Active"), ("completed", "Completed"), ("dropped", "Dropped")],
        default="active",
    )

    class Meta:
        unique_together = ("student", "course")  # prevent duplicate enrollments

    def __str__(self):
        return f"{self.student.username} → {self.course.code}"
