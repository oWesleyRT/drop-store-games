import { Component, inject, signal, computed, OnInit } from '@angular/core';
import { HeroBanner } from '../../components/hero-banner/hero-banner';
import { CategoryFilter } from '../../components/category-filter/category-filter';
import { SearchBar } from '../../components/search-bar/search-bar';
import { GameList } from '../../components/game-list/game-list';
import { GameService } from '../../services/game.service';
import { Game } from '../../models/game.model';

@Component({
  selector: 'app-home',
  imports: [HeroBanner, CategoryFilter, SearchBar, GameList],
  templateUrl: './home.html',
  styleUrl: './home.css'
})
export class Home implements OnInit {
  private readonly gameService = inject(GameService);

  allGames = signal<Game[]>([]);
  searchTerm = signal('');
  selectedCategory = signal('');
  categories: string[] = ['Ação', 'RPG', 'Aventura', 'Corrida', 'Esporte', 'Luta'];

  filteredGames = computed(() => {
    let games = this.allGames();
    const category = this.selectedCategory();
    const search = this.searchTerm().toLowerCase();

    if (category) {
      games = games.filter(g => g.categoria === category);
    }
    if (search) {
      games = games.filter(g => g.nome.toLowerCase().includes(search));
    }
    return games;
  });

  ngOnInit(): void {
    this.gameService.getGames().subscribe(games => {
      this.allGames.set(games);
    });
  }

  onCategoryChange(category: string): void {
    this.selectedCategory.set(category);
  }

  onSearchChange(term: string): void {
    this.searchTerm.set(term);
  }
}
