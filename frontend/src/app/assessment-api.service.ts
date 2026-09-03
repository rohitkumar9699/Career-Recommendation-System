import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class AssessmentApiService {
  private readonly http = inject(HttpClient);
  private readonly endpoint = '/api/assessment/submit/';

  submit(data: object): Observable<{ message: string; recommendations: string[] }> {
    const token = localStorage.getItem('access_token');
    const headers = new HttpHeaders({ Authorization: `Bearer ${token ?? ''}` });
    return this.http.post<{ message: string; recommendations: string[] }>(this.endpoint, data, { headers });
  }
}
