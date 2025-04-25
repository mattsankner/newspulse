import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatTableModule } from '@angular/material/table';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatButtonModule } from '@angular/material/button';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { FormsModule } from '@angular/forms';
import { ArticleService } from '../../services/article.service';
import { DataService } from '../../services/data.service';
import { Article, PoliticalStance } from '../../models/article.model';
import { HttpClientModule } from '@angular/common/http';
import { Subscription } from 'rxjs';
import { SelectionModel } from '@angular/cdk/collections';

@Component({
  selector: 'app-data-display-page',
  templateUrl: './data-display-page.component.html',
  styleUrls: ['./data-display-page.component.scss'],
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
    MatCheckboxModule,
    FormsModule,
    HttpClientModule
  ]
})
export class DataDisplayPageComponent implements OnInit, OnDestroy {
  articles: Article[] = [];
  filteredArticles: Article[] = [];
  savedArticles: Article[] = [];
  displayedColumns: string[] = ['select', 'title', 'description', 'source', 'published_at', 'political_stance'];
  selectedFilter: string = 'title';
  searchQuery: string = '';
  selectedStance: PoliticalStance | '' = '';
  hasData = false;
  isLoading = false;
  isSaving = false;
  showingSavedArticles = false;
  PoliticalStance = PoliticalStance;
  selection = new SelectionModel<Article>(true, []);

  private subscriptions: Subscription[] = [];

  constructor(
    private articleService: ArticleService,
    private dataService: DataService,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    // Subscribe to search results
    const resultsSub = this.dataService.currentSearchResults.subscribe(results => {
      this.filteredArticles = results;
      this.articles = results;
      this.hasData = results.length > 0;
      // Reset selection when new results arrive
      this.selection.clear();
    });

    this.subscriptions.push(resultsSub);

    // Load initial data if no search results
    if (!this.hasData) {
      this.loadArticles();
    }
  }

  ngOnDestroy(): void {
    this.subscriptions.forEach(sub => sub.unsubscribe());
  }

  /** Whether the number of selected elements matches the total number of rows. */
  isAllSelected() {
    const numSelected = this.selection.selected.length;
    const numRows = this.filteredArticles.length;
    return numSelected === numRows;
  }

  /** Selects all rows if they are not all selected; otherwise clear selection. */
  toggleAllRows() {
    if (this.isAllSelected()) {
      this.selection.clear();
      return;
    }

    this.selection.select(...this.filteredArticles);
  }

  loadArticles(): void {
    this.isLoading = true;
    this.articleService.getSavedArticles().subscribe({
      next: (articles) => {
        this.articles = articles;
        this.filteredArticles = articles;
        this.isLoading = false;
      },
      error: (error) => {
        console.error('Error loading articles:', error);
        this.isLoading = false;
      }
    });
  }

  loadSavedArticles(): void {
    this.isLoading = true;
    this.articleService.getSavedArticles(50, 0)
      .subscribe({
        next: (articles) => {
          this.savedArticles = articles;
          if (this.showingSavedArticles) {
            this.articles = articles;
          }
          this.hasData = articles.length > 0;
          this.isLoading = false;
          // Reset selection when loading saved articles
          this.selection.clear();
        },
        error: (error) => {
          console.error('Error loading saved articles:', error);
          this.isLoading = false;
          this.snackBar.open('Error loading saved articles', 'Close', { duration: 3000 });
        }
      });
  }

  toggleSavedArticles(): void {
    this.showingSavedArticles = !this.showingSavedArticles;
    if (this.showingSavedArticles) {
      this.loadSavedArticles();
    } else {
      this.articles = this.filteredArticles;
      this.hasData = this.filteredArticles.length > 0;
    }
    // Reset selection when toggling view
    this.selection.clear();
  }

  onFilterChange(): void {
    this.applyFilters();
  }

  onSearch(): void {
    this.applyFilters();
  }

  applyFilters(): void {
    if (!this.searchQuery) {
      this.filteredArticles = this.articles;
      return;
    }

    const query = this.searchQuery.toLowerCase();
    this.filteredArticles = this.articles.filter(article => {
      switch (this.selectedFilter) {
        case 'title':
          return article.title.toLowerCase().includes(query);
        case 'source_name':
          return article.source_name.toLowerCase().includes(query);
        case 'political_stance':
          return article.political_stance?.toLowerCase().includes(query) ?? false;
        case 'published_at':
          const date = new Date(article.published_at).toLocaleDateString();
          return date.includes(query);
        default:
          return true;
      }
    });
  }

  onStanceChange(): void {
    this.showingSavedArticles = false;
    this.loadArticles();
  }

  saveToDatabase(): void {
    const selectedArticles = this.selection.selected;
    
    if (selectedArticles.length === 0) {
      this.snackBar.open('Please select at least one article to save', 'Close', { duration: 3000 });
      return;
    }

    this.isSaving = true;
    
    // Format the articles to match the backend expected model
    const formattedArticles: Article[] = selectedArticles.map(article => {
      // Format the date as expected by the backend (ISO string with Z suffix)
      let publishedAt = article.published_at;
      if (publishedAt) {
        // Check if it's already a string in the correct format
        if (typeof publishedAt !== 'string' || !publishedAt.endsWith('Z')) {
          // Convert to ISO string
          const date = new Date(publishedAt);
          publishedAt = date.toISOString();
        }
      } else {
        publishedAt = new Date().toISOString();
      }

      return {
        id: article.id,
        title: article.title || '',
        description: article.description || '',
        url: typeof article.url === 'string' ? article.url : String(article.url || ''),
        source_name: article.source_name || '',
        published_at: publishedAt,
        content: article.content || '',
        source_id: article.source_id || '',
        author: article.author || '',
        url_to_image: article.url_to_image || '',
        political_stance: article.political_stance || '',
        classification: article.classification || undefined,
        raw_data: article.raw_data || {}
      };
    });
    
    console.log('Saving articles:', formattedArticles);
    
    this.articleService.saveArticlesToDatabase(formattedArticles)
      .subscribe({
        next: (response) => {
          console.log('Save response:', response);
          this.snackBar.open(response.message, 'View Saved', { duration: 3000 })
            .onAction().subscribe(() => {
              // Navigate to saved articles page when clicked
              window.location.href = '/saved-articles';
            });
          this.isSaving = false;
          // Clear selection after successful save
          this.selection.clear();
        },
        error: (error) => {
          console.error('Error saving articles:', error);
          this.snackBar.open('Error saving articles to database: ' + (error.message || 'Unknown error'), 'Close', { duration: 5000 });
          this.isSaving = false;
        }
      });
  }
} 