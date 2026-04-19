#!/usr/bin/env python3
"""
Gera anúncios formatados para OLX e Facebook Marketplace a partir do games.json.

Uso:
    python3 scripts/gerar_anuncios_v3.py
"""

import json
import os
import re
import unicodedata
from typing import Any, Dict, List

GAMES_JSON = os.path.join(
    os.path.dirname(__file__), "..", "src", "assets", "data", "games.json"
)

OUTPUT_OLX = os.path.join(os.path.dirname(__file__), "anuncios_olx.txt")
OUTPUT_MARKETPLACE = os.path.join(os.path.dirname(__file__), "anuncios_marketplace.txt")


def limpar_texto(texto: str) -> str:
    return re.sub(r"\s+", " ", (texto or "")).strip()


def remover_acentos(texto: str) -> str:
    normalized = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in normalized if not unicodedata.combining(c))


def formatar_preco(valor: float) -> str:
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def gerar_tag(nome: str) -> str:
    texto = remover_acentos(nome or "")
    texto = texto.lower()
    texto = re.sub(r"[^\w\s-]", "", texto)
    texto = texto.replace(" ", "-")
    return texto.strip("-")


def normalizar_condicao(condicao: str) -> str:
    cond = limpar_texto(condicao).lower()

    if cond in {"usado", "semi novo", "seminovo"}:
        return "Seminovo"
    if not cond:
        return "Seminovo"
    return limpar_texto(condicao)


def gerar_beneficios_midia_fisica() -> List[str]:
    return [
        "Não ocupa espaço de armazenamento do console como jogo digital",
        "Pode ser trocado ou revendido depois",
        "Pode ser usado em mais de um Nintendo Switch",
        "Ótima opção para coleção",
    ]


def gerar_titulo_olx(game: Dict[str, Any]) -> str:
    nome = limpar_texto(game.get("nome", "Jogo"))
    return f"{nome} Nintendo Switch Mídia Física"


def gerar_titulo_marketplace(game: Dict[str, Any]) -> str:
    nome = limpar_texto(game.get("nome", "Jogo"))
    return f"{nome} - Nintendo Switch - Mídia Física"


def gerar_descricao_base(game: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "nome": limpar_texto(game.get("nome", "Jogo")),
        "descricao": limpar_texto(game.get("descricao", "Jogo original para Nintendo Switch.")),
        "midia": limpar_texto(game.get("midia", "Física")),
        "condicao": normalizar_condicao(game.get("condicao", "Seminovo")),
        "preco": float(game.get("preco", 0) or 0),
        "categoria": limpar_texto(game.get("categoria", "Nintendo Switch")),
    }


def gerar_descricao_olx(game: Dict[str, Any], cidade_padrao: str = "Brasília") -> str:
    dados = gerar_descricao_base(game)
    beneficios = gerar_beneficios_midia_fisica()

    linhas = [
        f"{dados['nome']} para Nintendo Switch, mídia física, original e em ótimo estado.",
        "",
        dados["descricao"],
        "",
        "📦 Detalhes do produto:",
        "• Plataforma: Nintendo Switch",
        f"• Categoria: {dados['categoria']}",
        f"• Mídia: {dados['midia']}",
        f"• Condição: {dados['condicao']}",
        "• Jogo testado e funcionando normalmente",
        "",
        "🎮 Vantagens da mídia física:",
    ]

    for beneficio in beneficios:
        linhas.append(f"• {beneficio}")

    linhas.extend(
        [
            "",
            f"💰 Preço: R$ {formatar_preco(dados['preco'])}",
            "🔄 Avalio troca por outros jogos de Nintendo Switch.",
            "",
            f"📍 Retirada em mãos em {cidade_padrao} ou envio a combinar.",
            "📩 Me chama no chat que respondo rápido.",
            "",
            "🌐 Veja mais jogos em: www.dropstoregames.com.br",
        ]
    )

    return "\n".join(linhas).strip()


def gerar_descricao_marketplace(game: Dict[str, Any], cidade_padrao: str = "Brasília") -> str:
    dados = gerar_descricao_base(game)
    beneficios = gerar_beneficios_midia_fisica()

    linhas = [
        f"Vendo {dados['nome']} para Nintendo Switch, mídia física, original, em ótimo estado.",
        "",
        dados["descricao"],
        "",
        "Informações do produto:",
        f"- Plataforma: Nintendo Switch",
        f"- Categoria: {dados['categoria']}",
        f"- Mídia: {dados['midia']}",
        f"- Condição: {dados['condicao']}",
        f"- Jogo testado e funcionando normalmente",
        "",
        "Vantagens da mídia física:",
    ]

    for beneficio in beneficios:
        linhas.append(f"- {beneficio}")

    linhas.extend(
        [
            "",
            f"Preço: R$ {formatar_preco(dados['preco'])}",
            "Avalio troca por outros jogos de Nintendo Switch.",
            f"Retirada em mãos em {cidade_padrao} ou envio a combinar.",
            "Tenho outros jogos disponíveis também.",
            "Chama no chat se tiver interesse.",
        ]
    )

    return "\n".join(linhas).strip()


def gerar_bloco_olx(game: Dict[str, Any]) -> str:
    titulo = gerar_titulo_olx(game)
    preco = float(game.get("preco", 0) or 0)
    slug = game.get("slug") or gerar_tag(game.get("nome", "jogo"))
    descricao = gerar_descricao_olx(game)

    return (
        f"{'=' * 70}\n"
        f"ID: {game.get('id', '-')}\n"
        f"TÍTULO OLX: {titulo}\n"
        f"PREÇO: R$ {formatar_preco(preco)}\n"
        f"SLUG: {slug}\n"
        f"{'=' * 70}\n\n"
        f"{descricao}\n"
    )


def gerar_bloco_marketplace(game: Dict[str, Any]) -> str:
    titulo = gerar_titulo_marketplace(game)
    preco = float(game.get("preco", 0) or 0)
    slug = game.get("slug") or gerar_tag(game.get("nome", "jogo"))
    descricao = gerar_descricao_marketplace(game)

    return (
        f"{'=' * 70}\n"
        f"ID: {game.get('id', '-')}\n"
        f"TÍTULO MARKETPLACE: {titulo}\n"
        f"PREÇO: R$ {formatar_preco(preco)}\n"
        f"SLUG: {slug}\n"
        f"{'=' * 70}\n\n"
        f"{descricao}\n"
    )


def carregar_games(path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("O games.json deve conter uma lista de jogos.")

    return data


def salvar_arquivo(path: str, blocos: List[str]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(blocos))


def main() -> None:
    try:
        games = carregar_games(GAMES_JSON)
    except Exception as e:
        print(f"❌ Erro ao carregar games.json: {e}")
        return

    print("\n🎮 Gerador de anúncios OLX + Marketplace - DropStore")
    print(f"   {len(games)} jogos encontrados\n")

    blocos_olx: List[str] = []
    blocos_marketplace: List[str] = []

    for i, game in enumerate(games, start=1):
        try:
            bloco_olx = gerar_bloco_olx(game)
            bloco_marketplace = gerar_bloco_marketplace(game)

            blocos_olx.append(bloco_olx)
            blocos_marketplace.append(bloco_marketplace)

            print(f"[{i}] {game.get('nome', 'Jogo sem nome')} ✅")
        except Exception as e:
            print(f"⚠️ Erro ao gerar anúncio do item {i}: {e}")

    try:
        salvar_arquivo(OUTPUT_OLX, blocos_olx)
        salvar_arquivo(OUTPUT_MARKETPLACE, blocos_marketplace)

        print(f"\n✅ Arquivo OLX salvo em: {OUTPUT_OLX}")
        print(f"✅ Arquivo Marketplace salvo em: {OUTPUT_MARKETPLACE}")
    except Exception as e:
        print(f"\n❌ Erro ao salvar arquivos: {e}")


if __name__ == "__main__":
    main()