from django.urls import path
from student_app import views

urlpatterns=[
    path('', views.homeView)
]