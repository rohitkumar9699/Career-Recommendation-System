import { Component, EventEmitter, Input, Output, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { StudentApiService } from '../student-api.service';
import { Student } from '../models';

@Component({
  selector: 'app-update-profile',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './update-profile.component.html',
  styleUrl: './update-profile.component.css'
})
export class UpdateProfileComponent {
  private readonly studentApi = inject(StudentApiService);
  @Input({ required: true }) profile!: { name: string; mobile: string };
  @Output() cancel = new EventEmitter<void>();
  @Output() success = new EventEmitter<{ message: string; student: Student }>();
  @Output() failure = new EventEmitter<string>();

  update(): void {
    this.studentApi.updateDetails(this.profile).subscribe({
      next: response => this.success.emit(response),
      error: error => this.failure.emit(this.apiError(error, 'Profile update failed.'))
    });
  }

  private apiError(error: { error?: { message?: string; [key: string]: unknown } }, fallback: string): string {
    if (error.error?.message) return error.error.message;
    const details = error.error ? Object.values(error.error).flat().filter(Boolean) : [];
    return details.length ? details.join(' ') : fallback;
  }
}
