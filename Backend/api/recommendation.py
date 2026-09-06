import pickle
from pathlib import Path
import numpy as np
from django.db import transaction
from .models import CareerRoadmap
from .openai import generate_career_roadmap

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / 'model' / 'ourmodel.pkl'
SCALER_PATH = BASE_DIR / 'model' / 'scaler.pkl'


@transaction.atomic
def store_career_roadmaps(student, roadmap_data):
    """Store or update the roadmap recommendations for one student."""
    if student is None or not getattr(student, 'pk', None):
        raise ValueError('A saved student is required to store career roadmaps.')
    recommendations = roadmap_data.get('recommendations', [])
    if not isinstance(recommendations, list) or not recommendations:
        raise ValueError('roadmap_data must contain a non-empty recommendations list.')

    stored_roadmaps = []
    for recommendation in recommendations:
        required_fields = {
            'career', 'score', 'degree_course', 'what_you_do', 'skills', 'what_to_explore'
        }
        if not required_fields.issubset(recommendation):
            raise ValueError('Each roadmap recommendation must contain all required fields.')

        roadmap, _ = CareerRoadmap.objects.update_or_create(
            student=student,
            career=recommendation['career'],
            defaults={
                'score': float(recommendation['score']),
                'degree_course': recommendation['degree_course'],
                'what_you_do': recommendation['what_you_do'],
                'skills': recommendation['skills'],
                'what_to_explore': recommendation['what_to_explore'],
            },
        )
        stored_roadmaps.append(roadmap)

    return stored_roadmaps


def load_model_and_scaler():
    with open(SCALER_PATH, 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)
    with open(MODEL_PATH, 'rb') as model_file:
        model = pickle.load(model_file)
    return scaler, model


def generate_recommendations(gender, part_time_job, absence_days, extracurricular_activities,
                            weekly_self_study_hours, math_score, history_score, physics_score,
                            chemistry_score, biology_score, english_score, geography_score,
                            total_score, average_score,student):
    scaler, model = load_model_and_scaler()
    class_names = [
        'Lawyer', 'Doctor', 'Government Officer', 'Artist', 'Unknown', 'Software Engineer',
        'Teacher', 'Business Owner', 'Scientist', 'Banker', 'Writer', 'Accountant',
        'Designer', 'Construction Engineer', 'Game Developer', 'Stock Investor',
        'Real Estate Developer'
    ]

    gender_encoded = 1 if str(gender).lower() == 'female' else 0
    part_time_job_flag = 1 if bool(part_time_job) else 0
    extracurricular_flag = 1 if bool(extracurricular_activities) else 0

    feature_array = np.array([[
        gender_encoded, part_time_job_flag, int(absence_days), extracurricular_flag,
        int(weekly_self_study_hours), int(math_score), int(history_score), int(physics_score),
        int(chemistry_score), int(biology_score), int(english_score), int(geography_score),
        int(total_score), float(average_score)
    ]])

    scaled_features = scaler.transform(feature_array)
    probabilities = model.predict_proba(scaled_features)
    top_classes_idx = np.argsort(-probabilities[0])[:4]
    top_classes_names_probs = [(class_names[idx], float(probabilities[0][idx])) for idx in top_classes_idx]
    result = [name for name, _ in top_classes_names_probs if name != 'Unknown']
    recommendations = [{'career': name, 'score': prob} for name, prob in top_classes_names_probs if name != 'Unknown']
    print("Recommendations:", recommendations)

    try:
        data = generate_career_roadmap(recommendations)
        store_career_roadmaps(student, data)
    except Exception as e:
        print(f"Error occurred while generating career roadmaps: {e}")

    while len(result) < 3:
        result.append('Not Recommended Yet')
    return result[:3]
