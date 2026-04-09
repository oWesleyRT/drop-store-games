export interface Game {
  id: number;
  slug: string;
  nome: string;
  categoria: string;
  preco: number;
  precoOriginal?: number;
  imagem: string;
  descricao: string;
  condicao: string;
  midia: string;
}
