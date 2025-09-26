from django.urls import path
from student_app import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('',views.HomeView),
     path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
     path('profile/', views.profile_view, name='profile'),
      path("profile/edit/", views.edit_profile, name="edit_profile"),
]