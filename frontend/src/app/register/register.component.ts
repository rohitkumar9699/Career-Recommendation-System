import { Component, EventEmitter, Output, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AuthApiService } from '../auth-api.service';
import { PublicView } from '../welcome/welcome.component';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {
  private readonly authApi = inject(AuthApiService);
  @Output() navigate = new EventEmitter<PublicView>();
  @Output() success = new EventEmitter<{ message: string; email: string }>();
  @Output() failure = new EventEmitter<string>();
  registerData = { username: '', email: '', password: '', mobile: '', gender: 'male' };

  submit(): void {
    this.authApi.register(this.registerData).subscribe({
      next: response => this.success.emit({ message: response.message, email: this.registerData.email }),
      error: error => this.failure.emit(this.apiError(error, 'Registration failed.'))
    });
  }

  private apiError(error: { error?: { message?: string; [key: string]: unknown } }, fallback: string): string {
    if (error.error?.message) return error.error.message;
    const details = error.error ? Object.values(error.error).flat().filter(Boolean) : [];
    return details.length ? details.join(' ') : fallback;
  }
}
