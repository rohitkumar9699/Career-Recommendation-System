import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { AppComponent } from './app.component';
import { AssessmentComponent } from './assessment/assessment.component';

describe('AppComponent', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AppComponent],
      providers: [provideHttpClient()],
    }).compileComponents();
  });

  it('starts on the welcome view', () => {
    const fixture = TestBed.createComponent(AppComponent);
    expect(fixture.componentInstance.view).toBe('welcome');
  });

  it('calculates total and average assessment scores', () => {
    const fixture = TestBed.createComponent(AssessmentComponent);
    const assessment = fixture.componentInstance;
    assessment.assessment.math_score = 70;
    assessment.assessment.history_score = 80;
    assessment.assessment.physics_score = 90;
    assessment.assessment.chemistry_score = 60;
    assessment.assessment.biology_score = 75;
    assessment.assessment.english_score = 85;
    assessment.assessment.geography_score = 70;

    assessment.calculateScores();

    expect(assessment.assessment.total_score).toBe(530);
    expect(assessment.assessment.average_score).toBe(75.71);
  });
});
