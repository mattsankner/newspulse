import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { Article } from '../../models/article.model';

@Component({
  selector: 'app-article-card',
  templateUrl: './article-card.component.html',
  styleUrls: ['./article-card.component.scss'],
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule
  ]
})
export class ArticleCardComponent {
  @Input() article: Article = {
    id: '',
    title: '',
    description: '',
    content: '',
    url: '',
    source_id: '',
    source_name: '',
    author: '',
    published_at: '',
    url_to_image: ''
  };
}
