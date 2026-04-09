import { Routes } from '@angular/router';
import { Home } from './pages/home/home';
import { GameDetail } from './pages/game-detail/game-detail';

export const routes: Routes = [
  { path: '', component: Home },
  { path: 'jogo/:slug', component: GameDetail },
  { path: '**', redirectTo: '' }
];
