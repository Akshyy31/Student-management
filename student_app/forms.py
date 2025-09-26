from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,StudentProfile

class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", 'first_name','last_name',"email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "student"   # ensure role is student
        if commit:
            user.save()
            # Create profile right here
            StudentProfile.objects.create(user=user)
        return user
    
from django.contrib.auth import get_user_model
CustomUser = get_user_model()

class StudentFullProfileForm(forms.ModelForm):
    # Fields from CustomUser (manual)
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = StudentProfile
        fields = ['profile_picture', 'date_of_birth', 'year_of_admission']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email
            self.user_instance = user

    def save(self, commit=True):
        profile = super().save(commit=False)

        # Save data to CustomUser
        self.user_instance.username = self.cleaned_data['username']
        self.user_instance.email = self.cleaned_data['email']

        if commit:
            self.user_instance.save()
            profile.user = self.user_instance
            profile.save()

        return profile