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
import { PoliticalStanceService } from '../../services/political-stance.service';
import { Article, PoliticalStance } from '../../models/article.model';

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
    RightColumnComponent
  ]
})
export class DashboardComponent {
  hasData = false;
  searchQuery = '';
  
  constructor(
    private articleService: ArticleService,
    private politicalStanceService: PoliticalStanceService
  ) {}
  
  searchTopics(): void {
    if (!this.searchQuery.trim()) return;
    
    this.articleService.getArticles(undefined, this.searchQuery)
      .subscribe(articles => {
        this.hasData = articles.length > 0;
        // TODO: Pass articles to child components
      });
  }
  
  exportCsv(): void {
    this.articleService.exportCsv(undefined, this.searchQuery)
      .subscribe(blob => {
        // TODO: Handle CSV download
      });
  }
}
