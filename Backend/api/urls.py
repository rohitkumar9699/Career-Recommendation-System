from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health_check'),
    path('register/', views.register_student, name='register_student'),
    path('login/', views.login_student, name='login_student'),
    path('students/me/', views.student_profile, name='student_profile'),
    path('students/update/', views.update_student_profile, name='update_student_profile'),
    path('assessment/submit/', views.submit_assessment, name='submit_assessment'),
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/students/', views.admin_students, name='admin_students'),
    path('admin/search/', views.admin_search_student, name='admin_search_student'),
    path('admin/delete/', views.admin_delete_student, name='admin_delete_student'),
]
