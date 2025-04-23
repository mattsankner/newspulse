import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { Classification } from '../models/article.model';

export interface Consensus {
  id: number;
  topic: string;
  summary: string;
  left_points: string[];
  center_points: string[];
  right_points: string[];
  common_ground: string[];
}

@Injectable({
  providedIn: 'root'
})
export class StanceService {
  constructor(private http: HttpClient) {}

  getConsensus(topic: string): Observable<Consensus> {
    // Mock data for initial development
    return of({
      id: 1,
      topic: topic,
      summary: `Summary of political positions on ${topic}`,
      left_points: [
        `Left perspective on ${topic} - point 1`,
        `Left perspective on ${topic} - point 2`
      ],
      center_points: [
        `Center perspective on ${topic} - point 1`,
        `Center perspective on ${topic} - point 2`
      ],
      right_points: [
        `Right perspective on ${topic} - point 1`,
        `Right perspective on ${topic} - point 2`
      ],
      common_ground: [
        `Common ground on ${topic} - point 1`,
        `Common ground on ${topic} - point 2`
      ]
    });
  }
}
