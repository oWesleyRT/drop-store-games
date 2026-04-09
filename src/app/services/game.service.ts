import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map, shareReplay } from 'rxjs';
import { Game } from '../models/game.model';

@Injectable({ providedIn: 'root' })
export class GameService {
  private readonly http = inject(HttpClient);
  private readonly gamesUrl = 'assets/data/games.json';
  private games$ = this.http.get<Game[]>(this.gamesUrl).pipe(shareReplay(1));

  getGames(): Observable<Game[]> {
    return this.games$;
  }

  getGameBySlug(slug: string): Observable<Game | undefined> {
    return this.games$.pipe(
      map(games => games.find(g => g.slug === slug))
    );
  }

  filterByCategory(category: string): Observable<Game[]> {
    return this.games$.pipe(
      map(games => games.filter(g => g.categoria === category))
    );
  }

  searchByName(term: string): Observable<Game[]> {
    const lower = term.toLowerCase();
    return this.games$.pipe(
      map(games => games.filter(g => g.nome.toLowerCase().includes(lower)))
    );
  }
}
