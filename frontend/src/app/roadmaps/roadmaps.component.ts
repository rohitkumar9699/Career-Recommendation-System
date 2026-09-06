import { CommonModule } from '@angular/common';
import { Component, Input, OnInit } from '@angular/core';
import { CareerRoadmap, Student } from '../models';
import { StudentApiService } from '../student-api.service';

@Component({
  selector: 'app-roadmaps',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './roadmaps.component.html',
  styleUrl: './roadmaps.component.css'
})
export class RoadmapsComponent implements OnInit {
  @Input({ required: true }) student!: Student;

  roadmaps: CareerRoadmap[] = [];
  isLoading = true;

  constructor(private readonly studentApi: StudentApiService) {}

  ngOnInit(): void {
    if (!this.student) {
      this.isLoading = false;
      return;
    }

    this.studentApi.roadmaps().subscribe({
      next: (response) => {
        this.roadmaps = response;
        this.isLoading = false;
      },
      error: () => {
        this.roadmaps = [];
        this.isLoading = false;
      }
    });
  }
}
