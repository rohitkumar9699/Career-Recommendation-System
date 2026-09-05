import { Component, EventEmitter, Output, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AuthApiService, AuthResponse } from '../auth-api.service';
import { PublicView } from '../welcome/welcome.component';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  private readonly authApi = inject(AuthApiService);
  @Output() navigate = new EventEmitter<PublicView>();
  @Output() success = new EventEmitter<AuthResponse>();
  @Output() failure = new EventEmitter<string>();
  loginData = { email: '', password: '' };

  submit(): void {
    this.authApi.login(this.loginData).subscribe({
      next: response => this.success.emit(response),
      error: error => this.failure.emit(this.apiError(error, 'Unable to sign in.'))
    });
  }

  private apiError(error: { error?: { message?: string; [key: string]: unknown } }, fallback: string): string {
    if (error.error?.message) return error.error.message;
    const details = error.error ? Object.values(error.error).flat().filter(Boolean) : [];
    return details.length ? details.join(' ') : fallback;
  }
}
