import { Component, input, output } from '@angular/core';

@Component({
  selector: 'app-category-filter',
  templateUrl: './category-filter.html',
  styleUrl: './category-filter.css'
})
export class CategoryFilter {
  categories = input.required<string[]>();
  selected = input<string>('');
  categoryChange = output<string>();

  onSelect(category: string): void {
    this.categoryChange.emit(category === this.selected() ? '' : category);
  }
}
