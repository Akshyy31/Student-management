from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Course


class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

    # Correct indentation: save() must be outside Meta
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "student"   # ensure role is student
        if commit:
            user.save()
        return user


class StudentFullProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "profile_picture",
            "date_of_birth",
            "year_of_admission",
        ]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class AdminAddStudentForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username","first_name", "last_name", "email"]

    def save(self, commit=True):
        student = super().save(commit=False)
        student.role = "student"   # force role
        student.set_password("student123")  # default password
        if commit:
            student.save()
        return student
    
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["name", "code", "description", "credits"]
    