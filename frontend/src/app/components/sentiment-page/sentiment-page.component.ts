import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-sentiment-page',
  template: `
    <div class="sentiment-page">
      <h1>Sentiment Analysis</h1>
      <p>This page will display articles organized by political sentiment. Coming soon!</p>
    </div>
  `,
  styles: [`
    .sentiment-page {
      padding: 2rem;
      text-align: center;
      
      h1 {
        color: #333;
        margin-bottom: 1rem;
      }
      
      p {
        color: #666;
      }
    }
  `],
  standalone: true,
  imports: [CommonModule]
})
export class SentimentPageComponent {} 