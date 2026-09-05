from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AssessmentResult, Student


def set_default_recommendations(student):
	default_recommendation = 'Not Recommended Yet'
	for field in ('recommendation_1', 'recommendation_2', 'recommendation_3'):
		if not getattr(student, field):
			setattr(student, field, default_recommendation)
	student.save(update_fields=('recommendation_1', 'recommendation_2', 'recommendation_3'))


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

	def save_model(self, request, obj, form, change):
		super().save_model(request, obj, form, change)
		set_default_recommendations(obj)


@admin.register(AssessmentResult)
class AssessmentResultAdmin(admin.ModelAdmin):
	list_display = ('student', 'total_score', 'average_score', 'absence_days', 'weekly_self_study_hours')
	search_fields = ('student__username', 'student__email')
	list_filter = ('gender', 'part_time_job', 'extracurricular_activities')

	def save_model(self, request, obj, form, change):
		super().save_model(request, obj, form, change)
		set_default_recommendations(obj.student)

	def delete_model(self, request, obj):
		student = obj.student
		super().delete_model(request, obj)
		student.recommendation_1 = 'Not Recommended Yet'
		student.recommendation_2 = 'Not Recommended Yet'
		student.recommendation_3 = 'Not Recommended Yet'
		set_default_recommendations(student)

	def delete_queryset(self, request, queryset):
		students = [assessment.student for assessment in queryset.select_related('student')]
		super().delete_queryset(request, queryset)
		for student in students:
			student.recommendation_1 = 'Not Recommended Yet'
			student.recommendation_2 = 'Not Recommended Yet'
			student.recommendation_3 = 'Not Recommended Yet'
			set_default_recommendations(student)

