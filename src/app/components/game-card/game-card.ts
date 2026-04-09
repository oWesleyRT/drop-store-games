import { Component, input } from '@angular/core';
import { RouterLink } from '@angular/router';
import { CurrencyPipe } from '@angular/common';
import { Game } from '../../models/game.model';

@Component({
  selector: 'app-game-card',
  imports: [RouterLink, CurrencyPipe],
  templateUrl: './game-card.html',
  styleUrl: './game-card.css'
})
export class GameCard {
  game = input.required<Game>();

  getWhatsAppUrl(): string {
    const message = encodeURIComponent(
      `Olá! Tenho interesse no jogo ${this.game().nome}. Ele ainda está disponível?`
    );
    return `https://wa.me/5535998082198?text=${message}`;
  }

  onImageError(event: Event): void {
    (event.target as HTMLImageElement).style.display = 'none';
  }
}
