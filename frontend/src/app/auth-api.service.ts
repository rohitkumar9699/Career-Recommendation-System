import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Student } from './models';

export interface AuthResponse {
  message: string;
  student: Student;
  tokens: { access: string; refresh: string };
}

@Injectable({ providedIn: 'root' })
export class AuthApiService {
  private readonly http = inject(HttpClient);
  private readonly endpoint = '/api';

  register(data: object): Observable<{ message: string; student: Student }> {
    return this.http.post<{ message: string; student: Student }>(`${this.endpoint}/register/`, data);
  }

  login(data: object): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.endpoint}/login/`, data);
  }
}
