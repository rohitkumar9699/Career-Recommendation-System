export interface Student {
  id: number;
  username: string;
  email: string;
  mobile: string;
  gender: string;
  recommendation_1: string;
  recommendation_2: string;
  recommendation_3: string;
  assessment_result: {
    absence_days: number;
    weekly_self_study_hours: number;
    total_score: number;
    average_score: number;
    math_score: number;
    history_score: number;
    physics_score: number;
    chemistry_score: number;
    biology_score: number;
    english_score: number;
    geography_score: number;
  } | null;
}

export interface Assessment {
  [key: string]: string | number | boolean;
  gender: string;
  part_time_job: boolean;
  absence_days: number;
  extracurricular_activities: boolean;
  weekly_self_study_hours: number;
  math_score: number;
  history_score: number;
  physics_score: number;
  chemistry_score: number;
  biology_score: number;
  english_score: number;
  geography_score: number;
  total_score: number;
  average_score: number;
}
