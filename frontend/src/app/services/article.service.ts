import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { Article, PoliticalStance } from '../models/article.model';

@Injectable({
  providedIn: 'root'
})
export class ArticleService {
  private apiUrl = 'http://localhost:8000/api/v1';
  
  constructor(private http: HttpClient) { }
  
  getArticles(stance?: PoliticalStance, query?: string): Observable<Article[]> {
    // For Day 1, return mock data
    // Later this will connect to the API
    return of([]);
  }
  
  exportCsv(stance?: PoliticalStance, query?: string): Observable<Blob> {
    // For Day 1, this is a placeholder
    // Later this will connect to the API
    return of(new Blob());
  }
}
