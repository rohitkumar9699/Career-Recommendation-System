from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class Student(AbstractUser):
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=10)
    gender = models.CharField(max_length=50)
    recommendation_1 = models.CharField(max_length=100, default='Not Recommended Yet')
    recommendation_2 = models.CharField(max_length=100, default='Not Recommended Yet')
    recommendation_3 = models.CharField(max_length=100, default='Not Recommended Yet')
    status = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='student_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='student_user_permissions', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'mobile', 'gender']

    def __str__(self):
        return self.email


class AssessmentResult(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='assessment_result')
    gender = models.CharField(max_length=10)
    part_time_job = models.BooleanField()
    absence_days = models.IntegerField()
    extracurricular_activities = models.BooleanField()
    weekly_self_study_hours = models.IntegerField()
    math_score = models.IntegerField()
    history_score = models.IntegerField()
    physics_score = models.IntegerField()
    chemistry_score = models.IntegerField()
    biology_score = models.IntegerField()
    english_score = models.IntegerField()
    geography_score = models.IntegerField()
    total_score = models.IntegerField()
    average_score = models.FloatField()

    def __str__(self):
        return f'{self.student.email} - result'


class CareerRoadmap(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='career_roadmaps')
    career = models.CharField(max_length=100)
    score = models.FloatField()
    degree_course = models.JSONField(default=list)
    what_you_do = models.TextField()
    skills = models.JSONField(default=list)
    what_to_explore = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'career'], name='unique_student_career_roadmap'),
        ]
        ordering = ['-score', 'career']

    def __str__(self):
        return f'{self.student.email} - {self.career}'

