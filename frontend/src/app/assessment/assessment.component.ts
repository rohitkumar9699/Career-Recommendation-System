import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Output, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AssessmentApiService } from '../assessment-api.service';
import { Assessment } from '../models';

@Component({
  selector: 'app-assessment',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './assessment.component.html',
  styleUrl: './assessment.component.css'
})
export class AssessmentComponent {
  private readonly assessmentApi = inject(AssessmentApiService);
  @Output() success = new EventEmitter<{ message: string; student: import('../models').Student }>();
  @Output() failure = new EventEmitter<string>();
  @Output() submitting = new EventEmitter<boolean>();
  readonly subjects = ['math_score', 'history_score', 'physics_score', 'chemistry_score', 'biology_score', 'english_score', 'geography_score'] as const;
  isSubmitting = false;
  assessment: Assessment = { gender: 'male', part_time_job: false, absence_days: 0, extracurricular_activities: false, weekly_self_study_hours: 0, math_score: 0, history_score: 0, physics_score: 0, chemistry_score: 0, biology_score: 0, english_score: 0, geography_score: 0, total_score: 0, average_score: 0 };

  calculateScores(): void {
    this.assessment.total_score = this.subjects.reduce((total, subject) => total + Number(this.assessment[subject]), 0);
    this.assessment.average_score = Number((this.assessment.total_score / this.subjects.length).toFixed(2));
  }

  submit(): void {
    this.calculateScores();
    const invalidScore = this.subjects.find(subject => Number(this.assessment[subject]) < 0 || Number(this.assessment[subject]) > 100);
    if (invalidScore) {
      this.failure.emit('Each subject mark must be between 0 and 100.');
      return;
    }
    this.isSubmitting = true;
    this.submitting.emit(true);
    this.assessmentApi.submit(this.assessment).subscribe({
      next: response => { this.isSubmitting = false; this.submitting.emit(false); this.success.emit(response); },
      error: error => { this.isSubmitting = false; this.submitting.emit(false); this.failure.emit(this.apiError(error, 'Assessment submission failed.')); }
    });
  }

  private apiError(error: { error?: { message?: string; [key: string]: unknown } }, fallback: string): string {
    if (error.error?.message) return error.error.message;
    const details = error.error ? Object.values(error.error).flat().filter(Boolean) : [];
    return details.length ? details.join(' ') : fallback;
  }
}
