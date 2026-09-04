from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health_check'),
    path('register/', views.register_student, name='register_student'),
    path('login/', views.login_student, name='login_student'),
    path('students/me/', views.student_profile, name='student_profile'),
    path('students/update/', views.update_student_profile, name='update_student_profile'),
    path('assessment/submit/', views.submit_assessment, name='submit_assessment'),
]
