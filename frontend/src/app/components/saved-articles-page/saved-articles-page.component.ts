import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatTableModule } from '@angular/material/table';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatButtonModule } from '@angular/material/button';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { FormsModule } from '@angular/forms';
import { ArticleService } from '../../services/article.service';
import { Article } from '../../models/article.model';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-saved-articles-page',
  templateUrl: './saved-articles-page.component.html',
  styleUrls: ['./saved-articles-page.component.scss'],
  standalone: true,
  imports: [
    CommonModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatTableModule,
    MatIconModule,
    MatProgressSpinnerModule,
    MatButtonModule,
    MatSnackBarModule,
    FormsModule,
    HttpClientModule
  ]
})
export class SavedArticlesPageComponent implements OnInit {
  articles: Article[] = [];
  filteredArticles: Article[] = [];
  displayedColumns: string[] = ['title', 'description', 'source', 'published_at', 'political_stance'];
  selectedFilter: string = 'published_at';
  searchQuery: string = '';
  isLoading = false;
  
  constructor(
    private articleService: ArticleService,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.loadSavedArticles();
  }

  loadSavedArticles(): void {
    this.isLoading = true;
    this.articleService.getSavedArticles(100, 0)
      .subscribe({
        next: (articles) => {
          this.articles = articles;
          this.applyFilters();
          this.isLoading = false;
        },
        error: (error) => {
          console.error('Error loading saved articles:', error);
          this.isLoading = false;
          this.snackBar.open('Error loading saved articles', 'Close', { duration: 3000 });
        }
      });
  }

  onFilterChange(): void {
    this.applyFilters();
  }

  onSearch(): void {
    this.applyFilters();
  }

  applyFilters(): void {
    // First apply search
    if (!this.searchQuery) {
      this.filteredArticles = [...this.articles];
    } else {
      const query = this.searchQuery.toLowerCase();
      this.filteredArticles = this.articles.filter(article => 
        (article.title?.toLowerCase().includes(query) || article.description?.toLowerCase().includes(query))
      );
    }

    // Then apply sorting
    if (this.selectedFilter === 'title') {
      this.filteredArticles.sort((a, b) => (a.title || '').localeCompare(b.title || ''));
    } else if (this.selectedFilter === 'source_name') {
      this.filteredArticles.sort((a, b) => (a.source_name || '').localeCompare(b.source_name || ''));
    } else if (this.selectedFilter === 'published_at') {
      this.filteredArticles.sort((a, b) => {
        const dateA = new Date(a.published_at || 0);
        const dateB = new Date(b.published_at || 0);
        return dateB.getTime() - dateA.getTime(); // newest first
      });
    }
  }

  exportCsv(): void {
    const query = this.searchQuery ? this.searchQuery : undefined;
    
    this.articleService.exportCsv(undefined, query)
      .subscribe({
        next: (blob) => {
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = 'saved-articles.csv';
          document.body.appendChild(a);
          a.click();
          window.URL.revokeObjectURL(url);
          a.remove();
        },
        error: (error) => {
          console.error('Error exporting CSV:', error);
          this.snackBar.open('Error exporting CSV', 'Close', { duration: 3000 });
        }
      });
  }

  clearDatabase(): void {
    // Show confirmation dialog
    if (!confirm('Are you sure you want to clear all saved articles? This action cannot be undone.')) {
      return;
    }

    this.isLoading = true;
    this.articleService.clearDatabase()
      .subscribe({
        next: (response) => {
          this.snackBar.open(response.message, 'Close', { duration: 3000 });
          this.isLoading = false;
          // Reload the empty list
          this.articles = [];
          this.filteredArticles = [];
        },
        error: (error) => {
          console.error('Error clearing database:', error);
          this.snackBar.open('Error clearing database: ' + (error.message || 'Unknown error'), 'Close', { duration: 5000 });
          this.isLoading = false;
        }
      });
  }
}
