from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Course,Enrollment


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
        fields = ["title", "description"]

# forms.py
from django import forms
from .models import Enrollment, CustomUser, Course

# forms.py
from django import forms
from .models import Enrollment, CustomUser, Course

class EnrollmentForm(forms.ModelForm):
    student = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role='student'),
        label="Select Student"
    )
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        label="Select Course"
    )

    class Meta:
        model = Enrollment
        fields = ['student', 'course']


# forms.py
from django import forms
from .models import CustomUser, Course, Enrollment, Department

class StudentEditForm(forms.ModelForm):
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(), required=True
    )
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # can also use a dropdown with multiple select
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'department', 'courses']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['courses'].initial = self.instance.enrollments.values_list('course', flat=True)

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            user.enrollments.all().delete()  # remove old enrollments
            for course in self.cleaned_data['courses']:
                Enrollment.objects.create(student=user, course=course)
        return user
