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
  searchResults: Article[] = [];
  savedArticles: Article[] = [];
  displayedColumns: string[] = ['select', 'title', 'description', 'source', 'published_at', 'political_stance'];
  searchQuery = '';
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
      this.searchResults = results;
      if (!this.showingSavedArticles) {
        this.articles = results;
        this.hasData = results.length > 0;
      }
      // Reset selection when new results arrive
      this.selection.clear();
    });

    // Subscribe to search query
    const querySub = this.dataService.currentSearchQuery.subscribe(query => {
      this.searchQuery = query;
    });

    this.subscriptions.push(resultsSub, querySub);

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
    const numRows = this.articles.length;
    return numSelected === numRows;
  }

  /** Selects all rows if they are not all selected; otherwise clear selection. */
  toggleAllRows() {
    if (this.isAllSelected()) {
      this.selection.clear();
      return;
    }

    this.selection.select(...this.articles);
  }

  loadArticles(): void {
    this.isLoading = true;
    this.articleService.getArticles(this.selectedStance as PoliticalStance, this.searchQuery)
      .subscribe({
        next: (articles) => {
          this.searchResults = articles;
          if (!this.showingSavedArticles) {
            this.articles = articles;
          }
          this.hasData = articles.length > 0;
          this.isLoading = false;
          // Reset selection when loading new articles
          this.selection.clear();
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
      this.articles = this.searchResults;
      this.hasData = this.searchResults.length > 0;
    }
    // Reset selection when toggling view
    this.selection.clear();
  }

  onSearch(): void {
    this.showingSavedArticles = false;
    this.loadArticles();
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
      // Ensure URL is properly formatted - the most common issue
      // Convert any non-string URL to a string
      const url = typeof article.url === 'string' ? article.url : String(article.url);
      
      return {
        id: article.id,
        title: article.title,
        description: article.description,
        url: url,
        source_name: article.source_name,
        published_at: article.published_at,
        // Optional fields
        content: article.content,
        source_id: article.source_id,
        author: article.author,
        url_to_image: article.url_to_image,
        political_stance: article.political_stance,
        classification: article.classification,
        raw_data: article.raw_data || {}
      };
    });
    
    console.log('Saving articles:', formattedArticles);
    
    this.articleService.saveArticlesToDatabase(formattedArticles)
      .subscribe({
        next: (response) => {
          this.snackBar.open(response.message, 'Close', { duration: 3000 });
          this.isSaving = false;
          // Clear selection after successful save
          this.selection.clear();
          // Refresh saved articles if we're viewing them
          if (this.showingSavedArticles) {
            this.loadSavedArticles();
          }
        },
        error: (error) => {
          console.error('Error saving articles:', error);
          this.snackBar.open('Error saving articles to database', 'Close', { duration: 5000 });
          this.isSaving = false;
        }
      });
  }
} 