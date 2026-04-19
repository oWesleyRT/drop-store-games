#!/usr/bin/env python3
"""
Gera anúncios formatados para a OLX a partir do games.json.
Uso: python3 scripts/gerar_anuncios_olx.py
"""

import json
import os

GAMES_JSON = os.path.join(
    os.path.dirname(__file__), "..", "src", "assets", "data", "games.json"
)

TEMPLATE_TITULO = "{nome} - Nintendo Switch - Mídia Física"

def gerar_tag(nome: str) -> str:
    return nome.replace(" ", "").replace(":", "").replace("+", "").replace("®", "").replace("™", "")


def formatar_economia(game: dict) -> str:
    valor_nintendo = game.get("valorSiteNintendo", 0)
    if valor_nintendo > 0 and valor_nintendo > game["preco"]:
        economia = valor_nintendo - game["preco"]
        return f"🔥 Economia de R$ {economia:.2f} em relação à eShop (R$ {valor_nintendo:.2f})!\n"
    return ""


def gerar_descricao(game: dict) -> str:
    return f"""{game['nome']} - Nintendo Switch

{game['descricao']}

📦 Detalhes do produto:
• Plataforma: Nintendo Switch
• Mídia: {game['midia']}
• Condição: {game['condicao']}
• Jogo testado e funcionando perfeitamente

💰 Preço: R$ {game['preco']:.2f}
🔄 Posso aceitar troca em jogos de Switch, mediante avaliação!

📍 Envio para todo o Brasil ou retirada em mãos.
📩 Me chama no chat que respondo rápido!

🌐 Confira mais jogos em: www.dropstoregames.com.br"""


def gerar_anuncio(game: dict) -> str:
    titulo = TEMPLATE_TITULO.format(**game)
    descricao = gerar_descricao(game)
    return f"""{'=' * 60}
📋 TÍTULO: {titulo}
💲 PREÇO: R$ {game['preco']:.2f}
{'=' * 60}

{descricao}
"""


def main():
    with open(GAMES_JSON, encoding="utf-8") as f:
        games = json.load(f)

    print(f"\n🎮 Gerador de Anúncios OLX - DropStore")
    print(f"   {len(games)} jogos encontrados\n")

    output_lines = []
    for game in games:
        anuncio = gerar_anuncio(game)
        output_lines.append(anuncio)
        print(anuncio)

    output_path = os.path.join(os.path.dirname(__file__), "anuncios_olx.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))

    print(f"\n✅ Anúncios salvos em: {output_path}")


if __name__ == "__main__":
    main()
