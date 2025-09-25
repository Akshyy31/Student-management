from django.urls import path
from student_app import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('', views.HomeView),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
     path("register/", views.register, name="register"),
     path("profile/", views.profile, name="profile"),
]