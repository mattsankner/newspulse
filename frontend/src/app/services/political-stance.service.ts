import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { Consensus } from '../models/article.model';

@Injectable({
  providedIn: 'root'
})
export class PoliticalStanceService {
  private apiUrl = 'http://localhost:8000/api/v1';
  
  constructor(private http: HttpClient) { }
  
  getConsensus(topic: string): Observable<Consensus> {
    // For Day 1, return mock data
    // Later this will connect to the API
    return of({
      id: '1',
      topic: topic,
      summary: 'Placeholder consensus summary',
      left_points: ['Left point 1'],
      center_points: ['Center point 1'],
      right_points: ['Right point 1'],
      common_ground: ['Common ground 1']
    });
  }
} 