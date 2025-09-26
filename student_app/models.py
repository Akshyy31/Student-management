from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("student", "Student"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="student")

    def __str__(self):
        return f"{self.username} ({self.role})"


from django.db import models
from django.contrib.auth.models import User

# Department as a separate model
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True,default="Not assigned")

    def __str__(self):
        return self.name


class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)
   
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True,default="Not assigned")
    year_of_admission = models.IntegerField()
    date_of_birth = models.DateField(null=True, blank=True)  # ← Add this field
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.roll_number}"
