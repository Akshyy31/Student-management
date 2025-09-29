import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# ---------- Department Model ----------
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# ---------- Custom User Model ----------
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("student", "Student"),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="student")

    # Student-specific fields
    roll_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    year_of_admission = models.IntegerField(blank=True, null=True, default=2025)
    date_of_birth = models.DateField(null=True, blank=True, default=datetime.date(2000, 1, 1))
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
        default='profile_pics/default.png'
    )

    def __str__(self):
        return f"{self.username} ({self.role})"


# ---------- Course Model ----------
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)  # automatically set when created
    updated_at = models.DateTimeField(auto_now=True,null=True)      # automatically updated

    def __str__(self):
        return self.title


# ---------- Enrollment Model ----------
class Enrollment(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    enrollment_date = models.DateField(auto_now_add=True,null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    class Meta:
        unique_together = ('student', 'course')  # prevent duplicate enrollments

    def __str__(self):
        return f"{self.student.username} → {self.course.title} ({self.status})"
