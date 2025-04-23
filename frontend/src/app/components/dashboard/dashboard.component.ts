import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { LeftColumnComponent } from '../left-column/left-column.component';
import { CenterColumnComponent } from '../center-column/center-column.component';
import { RightColumnComponent } from '../right-column/right-column.component';
import { ArticleService } from '../../services/article.service';
import { StanceService } from '../../services/stance.service';
import { Article, PoliticalStance } from '../../models/article.model';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
  standalone: true,
  imports: [
    CommonModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    LeftColumnComponent,
    CenterColumnComponent,
    RightColumnComponent,
    FormsModule,
    HttpClientModule
  ],
  providers: [ArticleService, StanceService]
})
export class DashboardComponent {
  hasData = false;
  searchQuery = '';
  
  constructor(
    private articleService: ArticleService,
    private stanceService: StanceService
  ) {}
  
  searchTopics(): void {
    console.log('Searching for topics...');
    this.hasData = true; // For UI testing
  }
  
  exportCsv(): void {
    console.log('Exporting data as CSV...');
  }
}
