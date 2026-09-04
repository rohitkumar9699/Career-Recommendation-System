from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import AssessmentResult

Student = get_user_model()


class StudentSerializer(serializers.ModelSerializer):
    assessment_result = serializers.SerializerMethodField()

    def get_assessment_result(self, student):
        try:
            result = student.assessment_result
        except AssessmentResult.DoesNotExist:
            result = None
        if not result:
            return None
        return {
            'gender': result.gender,
            'part_time_job': result.part_time_job,
            'absence_days': result.absence_days,
            'extracurricular_activities': result.extracurricular_activities,
            'weekly_self_study_hours': result.weekly_self_study_hours,
            'math_score': result.math_score,
            'history_score': result.history_score,
            'physics_score': result.physics_score,
            'chemistry_score': result.chemistry_score,
            'biology_score': result.biology_score,
            'english_score': result.english_score,
            'geography_score': result.geography_score,
            'total_score': result.total_score,
            'average_score': result.average_score,
        }

    class Meta:
        model = Student
        fields = ['id', 'username', 'email', 'mobile', 'gender', 'recommendation_1', 'recommendation_2', 'recommendation_3', 'assessment_result']
        read_only_fields = ['id', 'recommendation_1', 'recommendation_2', 'recommendation_3']


class RegisterStudentSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Student
        fields = ['id', 'username', 'email', 'password', 'mobile', 'gender']

    def create(self, validated_data):
        password = validated_data.pop('password')
        student = Student(**validated_data)
        student.set_password(password)
        student.save()
        return student

    def validate_mobile(self, value):
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError('Mobile number must contain exactly 10 digits.')
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters long.')
        return value

