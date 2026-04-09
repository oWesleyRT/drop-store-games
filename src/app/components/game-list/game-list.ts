import { Component, input } from '@angular/core';
import { GameCard } from '../game-card/game-card';
import { Game } from '../../models/game.model';

@Component({
  selector: 'app-game-list',
  imports: [GameCard],
  templateUrl: './game-list.html',
  styleUrl: './game-list.css'
})
export class GameList {
  games = input.required<Game[]>();
}
