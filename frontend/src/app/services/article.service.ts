import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Article, PoliticalStance } from '../models/article.model';

@Injectable({
  providedIn: 'root'
})
export class ArticleService {
  private apiUrl = 'http://localhost:8000/api/v1/articles';

  constructor(private http: HttpClient) {}

  getArticles(stance?: PoliticalStance, search?: string): Observable<Article[]> {
    let url = this.apiUrl;
    const params: any = {};

    if (stance) {
      params.stance = stance;
    }
    if (search) {
      params.search = search;
    }

    return this.http.get<Article[]>(url, { params });
  }

  getTopHeadlines(): Observable<Article[]> {
    return this.http.post<Article[]>(`${this.apiUrl}/collect?category=politics`, {});
  }

  getArticlesByTopic(topic: string): Observable<Article[]> {
    return this.http.post<Article[]>(`${this.apiUrl}/collect?topic=${encodeURIComponent(topic)}`, {});
  }

  saveArticlesToDatabase(articles: Article[]): Observable<{ message: string }> {
    return this.http.post<{ message: string }>(`${this.apiUrl}/save`, articles);
  }

  getSavedArticles(limit: number = 10, offset: number = 0): Observable<Article[]> {
    return this.http.get<Article[]>(`${this.apiUrl}/saved?limit=${limit}&offset=${offset}`);
  }

  exportCsv(stance?: PoliticalStance, search?: string): Observable<Blob> {
    let url = `${this.apiUrl}/export`;
    const params: any = {};

    if (stance) {
      params.stance = stance;
    }
    if (search) {
      params.search = search;
    }

    return this.http.get(url, { params, responseType: 'blob' });
  }
}
