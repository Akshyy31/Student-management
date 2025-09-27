from django.urls import path
from student_app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.HomeView),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("students/", views.student_list, name="student_list"),
     path("students/add/", views.admin_add_student, name="add_student"),
     path("courses/", views.course_list, name="course_list"),
      path("courses/add/", views.add_course, name="add_course"),
]
