from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StudentProfile
         


from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, StudentProfile

@receiver(post_save, sender=CustomUser)
def create_student_profile(sender, instance, created, **kwargs):
    if created and instance.role == "student":  # only for students
        StudentProfile.objects.create(
            user=instance,
                                               # you can change this logic
            department="Not Assigned",         # default department
            year_of_admission=2025             # default year, can get from form
        )