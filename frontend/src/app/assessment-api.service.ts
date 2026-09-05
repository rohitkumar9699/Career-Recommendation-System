import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Student } from './models';

@Injectable({ providedIn: 'root' })
export class AssessmentApiService {
  private readonly http = inject(HttpClient);
  private readonly endpoint = '/api/assessment/submit/';

  submit(data: object): Observable<{ message: string; student: Student }> {
    const token = localStorage.getItem('access_token');
    const headers = new HttpHeaders({ Authorization: `Bearer ${token ?? ''}` });
    return this.http.post<{ message: string; student: Student }>(this.endpoint, data, { headers });
  }
}
