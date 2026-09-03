import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { AppComponent } from './app.component';

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
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;
    app.assessment.math_score = 70;
    app.assessment.history_score = 80;
    app.assessment.physics_score = 90;
    app.assessment.chemistry_score = 60;
    app.assessment.biology_score = 75;
    app.assessment.english_score = 85;
    app.assessment.geography_score = 70;

    app.calculateScores();

    expect(app.assessment.total_score).toBe(530);
    expect(app.assessment.average_score).toBe(75.71);
  });
});
