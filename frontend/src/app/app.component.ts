import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet, RouterLink } from '@angular/router';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    RouterOutlet,
    RouterLink,
    MatToolbarModule,
    MatButtonModule,
    MatIconModule
  ],
  template: `
    <mat-toolbar class="toolbar">
      <span class="title">Political Content Analyzer</span>
      <span class="spacer"></span>
      <nav class="nav-links">
        <a mat-button routerLink="/search" routerLinkActive="active">Search</a>
        <a mat-button routerLink="/data" routerLinkActive="active">Data</a>
        <a mat-button routerLink="/saved-articles" routerLinkActive="active">Saved Articles</a>
        <a mat-button routerLink="/sentiment" routerLinkActive="active">Sentiment</a>
        <a mat-button routerLink="/dashboard" routerLinkActive="active">Dashboard</a>
      </nav>
    </mat-toolbar>
    <div class="content">
      <router-outlet></router-outlet>
    </div>
  `,
  styles: [`
    .toolbar {
      background-color: #8B4513; /* Saddle Brown */
      color: #F5F5DC; /* Beige */
    }

    .title {
      font-family: 'Georgia', serif;
      font-size: 1.5rem;
      font-weight: bold;
    }

    .spacer {
      flex: 1 1 auto;
    }

    .nav-links {
      display: flex;
      gap: 1rem;
    }

    .nav-links a {
      color: #F5F5DC;
      text-decoration: none;
      font-family: 'Georgia', serif;
      transition: color 0.3s ease;
    }

    .nav-links a:hover {
      color: #DEB887; /* Burlywood */
    }

    .nav-links a.active {
      color: #DEB887;
      border-bottom: 2px solid #DEB887;
    }

    .content {
      padding: 20px;
      background-color: #F5F5DC;
      min-height: calc(100vh - 64px);
    }
  `]
})
export class AppComponent {
  title = 'Political Content Analyzer';
}
