import pickle
from pathlib import Path
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / 'model' / 'ourmodel.pkl'
SCALER_PATH = BASE_DIR / 'model' / 'scaler.pkl'


def load_model_and_scaler():
    with open(SCALER_PATH, 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)
    with open(MODEL_PATH, 'rb') as model_file:
        model = pickle.load(model_file)
    return scaler, model


def generate_recommendations(gender, part_time_job, absence_days, extracurricular_activities,
                            weekly_self_study_hours, math_score, history_score, physics_score,
                            chemistry_score, biology_score, english_score, geography_score,
                            total_score, average_score):
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
    while len(result) < 3:
        result.append('Not Recommended Yet')
    return result[:3]
