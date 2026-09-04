import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Student } from './models';

@Injectable({ providedIn: 'root' })
export class StudentApiService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = '/api';

  private headers(): HttpHeaders {
    const token = localStorage.getItem('access_token');
    return new HttpHeaders({ Authorization: `Bearer ${token ?? ''}` });
  }

  profile(): Observable<Student> {
    return this.http.get<Student>(`${this.baseUrl}/students/me/`, { headers: this.headers() });
  }

  updateDetails(data: { name: string; mobile: string }): Observable<{ message: string; student: Student }> {
    return this.http.put<{ message: string; student: Student }>(`${this.baseUrl}/students/update/`, data, { headers: this.headers() });
  }
}
