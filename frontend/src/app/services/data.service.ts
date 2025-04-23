import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { Article } from '../models/article.model';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  private searchResults = new BehaviorSubject<Article[]>([]);
  currentSearchResults = this.searchResults.asObservable();

  private searchQuery = new BehaviorSubject<string>('');
  currentSearchQuery = this.searchQuery.asObservable();

  updateSearchResults(results: Article[]): void {
    this.searchResults.next(results);
  }

  updateSearchQuery(query: string): void {
    this.searchQuery.next(query);
  }

  clearSearch(): void {
    this.searchResults.next([]);
    this.searchQuery.next('');
  }
} 