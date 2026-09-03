import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

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

@Injectable({ providedIn: 'root' })
export class ApiService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = '/api';

  private authHeaders(): HttpHeaders {
    const token = localStorage.getItem('access_token');
    return token ? new HttpHeaders({ Authorization: `Bearer ${token}` }) : new HttpHeaders();
  }

  register(data: object): Observable<{ message: string; student: Student }> {
    return this.http.post<{ message: string; student: Student }>(`${this.apiUrl}/register/`, data);
  }

  login(data: object): Observable<{ message: string; student: Student; tokens: { access: string; refresh: string } }> {
    return this.http.post<{ message: string; student: Student; tokens: { access: string; refresh: string } }>(`${this.apiUrl}/login/`, data);
  }

  profile(): Observable<Student> {
    return this.http.get<Student>(`${this.apiUrl}/students/me/`, { headers: this.authHeaders() });
  }

  updateProfile(data: object): Observable<{ message: string; student: Student }> {
    return this.http.put<{ message: string; student: Student }>(`${this.apiUrl}/students/update/`, data, { headers: this.authHeaders() });
  }

  submitAssessment(data: object): Observable<{ message: string; recommendations: string[] }> {
    return this.http.post<{ message: string; recommendations: string[] }>(`${this.apiUrl}/assessment/submit/`, data, { headers: this.authHeaders() });
  }

  adminLogin(data: object): Observable<{ message: string; admin: { admin_name: string; admin_email: string } }> {
    return this.http.post<{ message: string; admin: { admin_name: string; admin_email: string } }>(`${this.apiUrl}/admin/login/`, data);
  }

  students(): Observable<Student[]> {
    return this.http.get<Student[]>(`${this.apiUrl}/admin/students/`);
  }

  searchStudent(email: string): Observable<Student> {
    return this.http.post<Student>(`${this.apiUrl}/admin/search/`, { email });
  }

  deleteStudent(id: number): Observable<{ message: string }> {
    return this.http.post<{ message: string }>(`${this.apiUrl}/admin/delete/`, { student_id: id });
  }
}
