import { Component, inject, signal, OnInit } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { CurrencyPipe } from '@angular/common';
import { GameService } from '../../services/game.service';
import { Game } from '../../models/game.model';

@Component({
  selector: 'app-game-detail',
  imports: [RouterLink, CurrencyPipe],
  templateUrl: './game-detail.html',
  styleUrl: './game-detail.css'
})
export class GameDetail implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly gameService = inject(GameService);

  game = signal<Game | undefined>(undefined);
  loading = signal(true);

  ngOnInit(): void {
    const slug = this.route.snapshot.paramMap.get('slug');
    if (slug) {
      this.gameService.getGameBySlug(slug).subscribe(game => {
        this.game.set(game);
        this.loading.set(false);
      });
    }
  }

  getWhatsAppUrl(): string {
    const game = this.game();
    if (!game) return '';
    const message = encodeURIComponent(
      `Olá! Tenho interesse no jogo ${game.nome}. Ele ainda está disponível?`
    );
    return `https://wa.me/5535998082198?text=${message}`;
  }

  onImageError(event: Event): void {
    (event.target as HTMLImageElement).style.display = 'none';
  }
}
