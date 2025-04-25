import { Routes } from '@angular/router';
import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { SearchPageComponent } from './components/search-page/search-page.component';
import { DataDisplayPageComponent } from './components/data-display-page/data-display-page.component';
import { SavedArticlesPageComponent } from './components/saved-articles-page/saved-articles-page.component';
import { SentimentPageComponent } from './components/sentiment-page/sentiment-page.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { NotFoundPageComponent } from './components/not-found-page/not-found-page.component';

export const routes: Routes = [
  { path: '', redirectTo: '/search', pathMatch: 'full' },
  { path: 'search', component: SearchPageComponent },
  { path: 'data', component: DataDisplayPageComponent },
  { path: 'saved-articles', component: SavedArticlesPageComponent },
  { path: 'sentiment', component: SentimentPageComponent },
  { path: 'dashboard', component: DashboardComponent },
  { path: '**', component: NotFoundPageComponent }
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
  })
export class AppRoutingModule { }
