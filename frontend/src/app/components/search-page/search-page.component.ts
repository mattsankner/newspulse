import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatSelectModule } from '@angular/material/select';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatIconModule } from '@angular/material/icon';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ArticleService } from '../../services/article.service';
import { DataService } from '../../services/data.service';
import { Article } from '../../models/article.model';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-search-page',
  templateUrl: './search-page.component.html',
  styleUrls: ['./search-page.component.scss'],
  standalone: true,
  imports: [
    CommonModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatSelectModule,
    MatSnackBarModule,
    MatIconModule,
    FormsModule,
    HttpClientModule
  ]
})
export class SearchPageComponent {
  searchQuery = '';
  searchType: 'headlines' | 'topic' = 'headlines';

  constructor(
    private articleService: ArticleService,
    private dataService: DataService,
    private snackBar: MatSnackBar,
    private router: Router
  ) {}

  search(): void {
    if (!this.searchQuery.trim()) {
      this.snackBar.open('Please enter a search query', 'Close', { duration: 3000 });
      return;
    }

    this.dataService.updateSearchQuery(this.searchQuery);

    const searchObservable = this.searchType === 'headlines'
      ? this.articleService.getTopHeadlines()
      : this.articleService.getArticlesByTopic(this.searchQuery);

    searchObservable.subscribe({
      next: (articles: Article[]) => {
        this.dataService.updateSearchResults(articles);
        this.snackBar.open('Articles retrieved successfully!', 'View Data', { duration: 3000 })
          .onAction().subscribe(() => {
            this.router.navigate(['/data']);
          });
      },
      error: (error: Error) => {
        this.snackBar.open('Error retrieving articles: ' + error.message, 'Close', { duration: 5000 });
      }
    });
  }
} 