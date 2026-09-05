import { Component, EventEmitter, Output } from '@angular/core';

export type PublicView = 'welcome' | 'login' | 'register';

@Component({
  selector: 'app-welcome',
  standalone: true,
  templateUrl: './welcome.component.html',
  styleUrl: './welcome.component.css'
})
export class WelcomeComponent {
  @Output() navigate = new EventEmitter<PublicView>();
}
