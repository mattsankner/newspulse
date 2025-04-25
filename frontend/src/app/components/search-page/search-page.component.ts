import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatSelectModule } from '@angular/material/select';
import { MatSnackBar, MatSnackBarModule, MatSnackBarConfig } from '@angular/material/snack-bar';
import { MatIconModule } from '@angular/material/icon';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ArticleService } from '../../services/article.service';
import { DataService } from '../../services/data.service';
import { Article } from '../../models/article.model';
import { HttpClientModule } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';

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
export class SearchPageComponent implements OnInit {
  searchQuery = '';
  selectedSearchType: 'semantic' | 'keyword' = 'semantic';
  searchResults: Article[] = [];
  isLoading = false;

  constructor(
    private articleService: ArticleService,
    private dataService: DataService,
    private snackBar: MatSnackBar,
    private router: Router
  ) {}

  ngOnInit(): void {
    // Initialize any additional logic if needed
  }

  onSearchTypeChange(): void {
    // Reset search query when changing search type
    this.searchQuery = '';
  }

  private getSnackBarConfig(type: 'success' | 'error' = 'success'): MatSnackBarConfig {
    return {
      duration: type === 'error' ? 6000 : 4000,
      horizontalPosition: 'right',
      verticalPosition: 'top',
      panelClass: ['themed-snackbar', `${type}-snackbar`]
    };
  }

  async search(): Promise<void> {
    if (!this.searchQuery.trim()) {
      this.snackBar.open('Please enter a topic to search for', 'Got it', {
        ...this.getSnackBarConfig('error'),
        duration: 4000
      });
      return;
    }

    this.isLoading = true;
    try {
      const searchObservable = this.articleService.getArticlesByTopic(this.searchQuery);
      const results = await firstValueFrom(searchObservable);
      this.searchResults = results;
      this.dataService.updateSearchResults(results);
      
      const searchTypeLabel = this.selectedSearchType === 'semantic' ? 'semantic search' : 'keyword search';
      const resultCount = results.length;
      
      if (resultCount > 0) {
        const message = `✨ Found ${resultCount} ${resultCount === 1 ? 'result' : 'results'} using ${searchTypeLabel}`;
        const snackBarRef = this.snackBar.open(message, 'View Results', this.getSnackBarConfig('success'));
        
        snackBarRef.onAction().subscribe(() => {
          this.router.navigate(['/data-display']);
        });
      } else {
        const message = `🔍 No results found for "${this.searchQuery}" using ${searchTypeLabel}`;
        this.snackBar.open(message, 'Dismiss', this.getSnackBarConfig('success'));
      }
    } catch (error) {
      console.error('Search error:', error);
      this.snackBar.open(
        `⚠️ Unable to fetch articles: ${error instanceof Error ? error.message : 'Unknown error'}`,
        'Dismiss',
        this.getSnackBarConfig('error')
      );
    } finally {
      this.isLoading = false;
    }
  }
} 