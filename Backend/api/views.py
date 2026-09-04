from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as auth_login
from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import AssessmentResult
from .recommendation import generate_recommendations
from .serializers import RegisterStudentSerializer, StudentSerializer

Student = get_user_model()


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({'status': 'ok'})


@api_view(['POST'])
@permission_classes([AllowAny])
def register_student(request):
    serializer = RegisterStudentSerializer(data=request.data)
    if serializer.is_valid():
        try:
            student = serializer.save()
            return Response({'message': 'Registered successfully.', 'student': StudentSerializer(student).data}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'message': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_student(request):
    email = request.data.get('email')
    password = request.data.get('password')
    if not email or not password:
        return Response({'message': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
    student = authenticate(request, email=email, password=password)
    if student is not None:
        auth_login(request, student)
        return Response({'message': 'Login successful.', 'student': StudentSerializer(student).data, 'tokens': get_tokens_for_user(student)}, status=status.HTTP_200_OK)
    return Response({'message': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_profile(request):
    return Response(StudentSerializer(request.user).data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_student_profile(request):
    student = request.user
    name = request.data.get('name', student.username)
    mobile = request.data.get('mobile', student.mobile)
    if not name or not str(name).strip():
        return Response({'message': 'Name is required.'}, status=status.HTTP_400_BAD_REQUEST)
    if not str(mobile).isdigit() or len(str(mobile)) != 10:
        return Response({'message': 'Mobile number must contain exactly 10 digits.'}, status=status.HTTP_400_BAD_REQUEST)
    student.username = str(name).strip()
    student.mobile = str(mobile)
    student.save()
    return Response({'message': 'Successfully updated.', 'student': StudentSerializer(student).data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_assessment(request):
    student = request.user
    if AssessmentResult.objects.filter(student=student).exists():
        return Response({'message': 'Test is already taken.'}, status=status.HTTP_400_BAD_REQUEST)

    payload = request.data
    required_fields = ['gender', 'absence_days', 'weekly_self_study_hours', 'math_score', 'history_score', 'physics_score', 'chemistry_score', 'biology_score', 'english_score', 'geography_score']
    missing_fields = [field for field in required_fields if payload.get(field) in [None, '']]
    if missing_fields:
        return Response({'message': f'Missing required assessment fields: {", ".join(missing_fields)}.'}, status=status.HTTP_400_BAD_REQUEST)
    score_fields = ['math_score', 'history_score', 'physics_score', 'chemistry_score', 'biology_score', 'english_score', 'geography_score']
    try:
        invalid_scores = [field for field in score_fields if not 0 <= float(payload.get(field)) <= 100]
    except (TypeError, ValueError):
        return Response({'message': 'Each subject mark must be a number between 0 and 100.'}, status=status.HTTP_400_BAD_REQUEST)
    if invalid_scores:
        return Response({'message': f'Marks must be between 0 and 100: {", ".join(invalid_scores)}.'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        assessment = AssessmentResult.objects.create(
        student=student,
        gender=payload.get('gender', ''),
        part_time_job=payload.get('part_time_job') in ['true', 'True', True, 1, 'yes', 'Yes'],
        absence_days=int(payload.get('absence_days', 0)),
        extracurricular_activities=payload.get('extracurricular_activities') in ['true', 'True', True, 1, 'yes', 'Yes'],
        weekly_self_study_hours=int(payload.get('weekly_self_study_hours', 0)),
        math_score=int(payload.get('math_score', 0)),
        history_score=int(payload.get('history_score', 0)),
        physics_score=int(payload.get('physics_score', 0)),
        chemistry_score=int(payload.get('chemistry_score', 0)),
        biology_score=int(payload.get('biology_score', 0)),
        english_score=int(payload.get('english_score', 0)),
        geography_score=int(payload.get('geography_score', 0)),
        total_score=int(payload.get('total_score', 0)),
            average_score=float(payload.get('average_score', 0)),
        )
    except (TypeError, ValueError):
        return Response({'message': 'Assessment scores and activity values must be valid numbers.'}, status=status.HTTP_400_BAD_REQUEST)

    recommendations = generate_recommendations(
        gender=assessment.gender,
        part_time_job=assessment.part_time_job,
        absence_days=assessment.absence_days,
        extracurricular_activities=assessment.extracurricular_activities,
        weekly_self_study_hours=assessment.weekly_self_study_hours,
        math_score=assessment.math_score,
        history_score=assessment.history_score,
        physics_score=assessment.physics_score,
        chemistry_score=assessment.chemistry_score,
        biology_score=assessment.biology_score,
        english_score=assessment.english_score,
        geography_score=assessment.geography_score,
        total_score=assessment.total_score,
        average_score=assessment.average_score,
    )

    student.recommendation_1 = recommendations[0]
    student.recommendation_2 = recommendations[1]
    student.recommendation_3 = recommendations[2]
    student.save()

    return Response({'message': 'Submission successful.', 'recommendations': recommendations}, status=status.HTTP_200_OK)


