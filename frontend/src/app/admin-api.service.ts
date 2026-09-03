import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Student } from './api.service';

@Injectable({ providedIn: 'root' })
export class AdminApiService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = '/api/admin';

  login(data: object): Observable<{ message: string; admin: { admin_name: string; admin_email: string } }> {
    return this.http.post<{ message: string; admin: { admin_name: string; admin_email: string } }>(`${this.baseUrl}/login/`, data);
  }

  students(): Observable<Student[]> { return this.http.get<Student[]>(`${this.baseUrl}/students/`); }
  search(email: string): Observable<Student> { return this.http.post<Student>(`${this.baseUrl}/search/`, { email }); }
  delete(id: number): Observable<{ message: string }> { return this.http.post<{ message: string }>(`${this.baseUrl}/delete/`, { student_id: id }); }
}
