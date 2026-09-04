from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AssessmentResult, Student


@admin.register(Student)
class StudentAdmin(UserAdmin):
	list_display = ('id', 'username', 'email', 'mobile', 'gender', 'recommendation_1', 'recommendation_2', 'recommendation_3')
	search_fields = ('username', 'email', 'mobile')
	list_filter = ('gender', 'is_active')
	readonly_fields = ('last_login', 'date_joined')
	fieldsets = UserAdmin.fieldsets + (
		('Student details', {'fields': ('mobile', 'gender', 'recommendation_1', 'recommendation_2', 'recommendation_3', 'status')}),
	)
	add_fieldsets = UserAdmin.add_fieldsets + (
		('Student details', {'fields': ('email', 'mobile', 'gender')}),
	)


@admin.register(AssessmentResult)
class AssessmentResultAdmin(admin.ModelAdmin):
	list_display = ('student', 'total_score', 'average_score', 'absence_days', 'weekly_self_study_hours')
	search_fields = ('student__username', 'student__email')
	list_filter = ('gender', 'part_time_job', 'extracurricular_activities')

