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
    path('students/<int:student_id>/edit/', views.edit_student, name='edit_student'),
    path("courses/", views.course_list, name="course_list"),
    path("courses/add/", views.add_course, name="add_course"),
    path("courses/<int:pk>/edit/", views.edit_course, name="edit_course"),
    path("courses/<int:pk>/delete/", views.delete_course, name="delete_course"),
    path("enrollments/add/", views.add_enrollment, name="add_enrollment"),
    path("admin/student/<int:pk>/", views.student_detail, name="student_detail"),
    path("admin/student/edit/<int:pk>/", views.edit_student, name="edit_student"),
    path("assign-course/", views.assign_course, name="assign_course"),
    path("enrollments/", views.enrollment_list, name="enrollment_list"),
    path("edit-student/<int:student_id>/", views.edit_student, name="edit_student"),
    path("enrollment/<int:enrollment_id>/status/<str:status>/", views.update_enrollment_status, name="update_enrollment_status", ),
    path("enroll/<int:course_id>/", views.enroll_course, name="enroll_course")
]
