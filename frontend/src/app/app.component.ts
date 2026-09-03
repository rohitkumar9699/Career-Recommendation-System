import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Student } from './api.service';
import { AuthApiService } from './auth-api.service';
import { StudentApiService } from './student-api.service';
import { AssessmentApiService } from './assessment-api.service';
import { AdminApiService } from './admin-api.service';

interface Assessment {
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

interface AssessmentResult {
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
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  private readonly authApi = inject(AuthApiService);
  private readonly studentApi = inject(StudentApiService);
  private readonly assessmentApi = inject(AssessmentApiService);
  private readonly adminApi = inject(AdminApiService);
  view: 'welcome' | 'login' | 'register' | 'student' | 'assessment' | 'update' | 'admin' = 'welcome';
  darkMode = localStorage.getItem('theme') === 'dark';
  student: Student | null = null;
  admin: { admin_name: string; admin_email: string } | null = null;
  students: Student[] = [];
  selectedStudent: Student | null = null;
  message = '';
  error = '';
  isSubmitting = false;
  loginData = { email: '', password: '' };
  registerData = { username: '', email: '', password: '', mobile: '', gender: 'male' };
  profileData = { name: '', mobile: '' };
  adminData = { email: '', password: '' };
  searchEmail = '';
  assessment: Assessment = {
    gender: 'male', part_time_job: false, absence_days: 0, extracurricular_activities: false,
    weekly_self_study_hours: 0, math_score: 0, history_score: 0, physics_score: 0,
    chemistry_score: 0, biology_score: 0, english_score: 0, geography_score: 0,
    total_score: 0, average_score: 0
  };

  constructor() {
    const saved = localStorage.getItem('student');
    if (saved) {
      this.student = JSON.parse(saved);
      this.profileData = { name: this.student?.username ?? '', mobile: this.student?.mobile ?? '' };
      this.view = 'student';
      if (localStorage.getItem('access_token')) {
        this.studentApi.profile().subscribe({
          next: student => {
            this.student = student;
            this.profileData = { name: student.username, mobile: student.mobile };
            localStorage.setItem('student', JSON.stringify(student));
          },
          error: () => this.logout()
        });
      }
    }
  }

  go(view: 'welcome' | 'login' | 'register' | 'student' | 'assessment' | 'update' | 'admin') {
    this.clearStatus();
    this.view = view;
  }

  toggleTheme() {
    this.darkMode = !this.darkMode;
    localStorage.setItem('theme', this.darkMode ? 'dark' : 'light');
  }

  submitLogin() {
    this.clearStatus();
    this.authApi.login(this.loginData).subscribe({ next: response => {
      localStorage.setItem('access_token', response.tokens.access);
      localStorage.setItem('student', JSON.stringify(response.student));
      this.student = response.student;
      this.profileData = { name: response.student.username, mobile: response.student.mobile };
      this.view = 'student';
    }, error: error => this.error = this.apiError(error, 'Unable to sign in.') });
  }

  submitRegister() {
    this.clearStatus();
    this.authApi.register(this.registerData).subscribe({ next: response => {
      this.message = response.message;
      this.loginData.email = this.registerData.email;
      this.go('login');
      this.message = response.message;
    }, error: error => this.error = this.apiError(error, 'Registration failed.') });
  }

  loadAssessment() {
    this.clearStatus();
    if (this.student?.recommendation_1 !== 'Not Recommended Yet' && this.student?.recommendation_1 !== 'Not recommended yet') {
      this.error = 'You have already completed the assessment.';
      return;
    }
    this.go('assessment');
  }

  calculateScores() {
    const subjects = ['math_score', 'history_score', 'physics_score', 'chemistry_score', 'biology_score', 'english_score', 'geography_score'] as const;
    this.assessment.total_score = subjects.reduce((total, subject) => total + Number(this.assessment[subject]), 0);
    this.assessment.average_score = Number((this.assessment.total_score / subjects.length).toFixed(2));
  }

  submitAssessment() {
    this.clearStatus();
    this.calculateScores();
    const scoreFields = ['math_score', 'history_score', 'physics_score', 'chemistry_score', 'biology_score', 'english_score', 'geography_score'] as const;
    const invalidScore = scoreFields.find(field => Number(this.assessment[field]) < 0 || Number(this.assessment[field]) > 100);
    if (invalidScore) {
      this.error = 'Each subject mark must be between 0 and 100.';
      return;
    }
    this.isSubmitting = true;
    this.assessmentApi.submit(this.assessment).subscribe({ next: response => {
      this.isSubmitting = false;
      if (this.student) {
        this.student = { ...this.student, recommendation_1: response.recommendations[0], recommendation_2: response.recommendations[1], recommendation_3: response.recommendations[2] };
        localStorage.setItem('student', JSON.stringify(this.student));
      }
      this.message = response.message;
      this.view = 'student';
    }, error: error => { this.isSubmitting = false; this.error = this.apiError(error, 'Assessment submission failed.'); } });
  }

  openUpdateDetails() {
    this.clearStatus();
    this.go('update');
  }

  updateProfile() {
    this.clearStatus();
    this.studentApi.updateDetails(this.profileData).subscribe({ next: response => {
      this.student = response.student;
      localStorage.setItem('student', JSON.stringify(response.student));
      this.message = response.message;
      this.view = 'student';
    }, error: error => this.error = this.apiError(error, 'Profile update failed.') });
  }

  submitAdminLogin() {
    this.clearStatus();
    this.adminApi.login(this.adminData).subscribe({ next: response => {
      this.admin = response.admin;
      this.loadStudents();
    }, error: error => this.error = this.apiError(error, 'Admin sign in failed.') });
  }

  loadStudents() {
    this.adminApi.students().subscribe({ next: students => { this.students = students; this.view = 'admin'; }, error: error => this.error = this.apiError(error, 'Unable to load student records.') });
  }

  searchStudent() {
    this.clearStatus();
    this.adminApi.search(this.searchEmail).subscribe({ next: student => this.selectedStudent = student, error: error => this.error = this.apiError(error, 'Student not found.') });
  }

  deleteStudent() {
    if (!this.selectedStudent) return;
    this.adminApi.delete(this.selectedStudent.id).subscribe({ next: response => {
      this.message = response.message;
      this.selectedStudent = null;
      this.loadStudents();
    }, error: error => this.error = this.apiError(error, 'Unable to delete student.') });
  }

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('student');
    this.student = null;
    this.admin = null;
    this.go('welcome');
  }

  private clearStatus() { this.message = ''; this.error = ''; }

  private apiError(error: { error?: { message?: string; [key: string]: unknown } }, fallback: string): string {
    if (error.error?.message) return error.error.message;
    const details = error.error ? Object.values(error.error).flat().filter(Boolean) : [];
    return details.length ? details.join(' ') : fallback;
  }
}
