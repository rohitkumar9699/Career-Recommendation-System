import { Component, inject, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Student } from './models';
import { StudentApiService } from './student-api.service';
import { WelcomeComponent } from './welcome/welcome.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { AssessmentComponent } from './assessment/assessment.component';
import { UpdateProfileComponent } from './update-profile/update-profile.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, WelcomeComponent, LoginComponent, RegisterComponent, DashboardComponent, AssessmentComponent, UpdateProfileComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
  encapsulation: ViewEncapsulation.None
})
export class AppComponent {
  private readonly studentApi = inject(StudentApiService);
  view: 'welcome' | 'login' | 'register' | 'student' | 'assessment' | 'update' = 'welcome';
  darkMode = localStorage.getItem('theme') === 'dark';
  student: Student | null = null;
  message = '';
  error = '';
  isSubmitting = false;
  profileData = { name: '', mobile: '' };

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

  go(view: 'welcome' | 'login' | 'register' | 'student' | 'assessment' | 'update') {
    this.clearStatus();
    this.view = view;
  }

  toggleTheme() {
    this.darkMode = !this.darkMode;
    localStorage.setItem('theme', this.darkMode ? 'dark' : 'light');
  }

  handleLogin(response: { student: Student; tokens: { access: string } }) {
      localStorage.setItem('access_token', response.tokens.access);
      localStorage.setItem('student', JSON.stringify(response.student));
      this.student = response.student;
      this.profileData = { name: response.student.username, mobile: response.student.mobile };
      this.view = 'student';
      this.clearStatus();
  }

  handleRegister(response: { message: string; email: string }) {
      this.go('login');
      this.message = response.message;
  }

  loadAssessment() {
    this.clearStatus();
    if (this.student?.recommendation_1 !== 'Not Recommended Yet' && this.student?.recommendation_1 !== 'Not recommended yet') {
      this.error = 'You have already completed the assessment.';
      return;
    }
    this.go('assessment');
  }

  handleAssessment(response: { message: string; student: Student }) {
      this.student = response.student;
      localStorage.setItem('student', JSON.stringify(response.student));
      this.message = response.message;
      this.view = 'student';
      this.isSubmitting = false;
  }

  openUpdateDetails() {
    this.clearStatus();
    this.go('update');
  }

  handleProfileUpdate(response: { message: string; student: Student }) {
      this.student = response.student;
      localStorage.setItem('student', JSON.stringify(response.student));
      this.message = response.message;
      this.view = 'student';
  }

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('student');
    this.student = null;
    this.go('welcome');
  }

  private clearStatus() { this.message = ''; this.error = ''; }

}
