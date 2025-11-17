# Bibliotecas utilizadas
import pandas as pd
import re

# Função que limpa e normaliza um ingrediente individual.
# Remove números, medidas, caracteres especiais e palavras "de" isoladas.
#
# Parâmetros:
#   ing (str): texto do ingrediente
# Retorno:
#   string limpa contendo apenas o nome do ingrediente
def clean_ingredient(ing: str) -> str:
    ing = ing.lower()

    # Remove quantidades e unidades
    ing = re.sub(
        r"\b\d+[.,]?\d*\b", " ", ing
    )
    ing = re.sub(
        r"\b(ml|g|kg|mg|litro|xícara|xicara|colher|colheres|lata|latas|"
        r"unidade|unidades|pacote|pacotes|gramas?)\b", 
        " ", ing
    )

    # Remove adjetivos culinários comuns
    CULINARY_DESCRIPTORS = [
        "picado", "picada", "picados", "picadas",
        "fatiado", "fatiada",
        "ralado", "ralada",
        "moído", "moida", "moidos", "moidas",
        "triturado", "triturada",
        "cortado", "cortada", "em cubos", "em pedaços",
        "fresco", "fresca",
        "cozido", "cru", "crua",
        "temperado", "sem sal", "com sal"
    ]

    for desc in CULINARY_DESCRIPTORS:
        ing = ing.replace(desc, " ")

    # Remove símbolos e múltiplos espaços
    ing = re.sub(r"[^a-zA-Zà-ÿ\s]", " ", ing)
    ing = re.sub(r"\s+", " ", ing).strip()

    # Normalização por dicionário de equivalências
    NORMALIZATION_MAP = {
        "chocolate meio amargo": "chocolate",
        "chocolate ao leite": "chocolate",
        "chocolate amargo": "chocolate",
        "cacau em po": "cacau",
        "acucar refinado": "acucar",
        "acucar cristal": "acucar",
        "manteiga sem sal": "manteiga",
        "manteiga com sal": "manteiga",
        "farinha de trigo": "farinha",
        "farinha de milho fina": "farinha de milho",
        "oleo vegetal": "oleo",
        "ovo": "ovos",
        "noz": "nozes",
        "nozes picadas": "nozes",
        "suco de gengibre": "gengibre",
    }

    for k, v in NORMALIZATION_MAP.items():
        if ing == k or ing.startswith(k):
            ing = v

    # Remove "de" em excesso (mas mantém compostos reais ex: "água de coco")
    ing = re.sub(r"^de\s+|\s+de$", "", ing).strip()
    ing = re.sub(r"\s+", " ", ing)

    return ing

# Processamento da base SCRAPING (dict)
def preprocess_scraped_ingredients(data: dict) -> dict:
    # data: {prato: [ingredientes brutos]}
    processed = {}

    for prato, ingredientes in data.items():
        limpos = []
        for ing in ingredientes:
            if isinstance(ing, str) and ing.strip():
                limpos.append(clean_ingredient(ing))

        # remove duplicados
        limpos = sorted(list(set(limpos)))

        processed[prato.lower().strip()] = limpos

    return processed


def make_scraping_text_data(data: dict) -> dict:
    # retorna lista de ingredientes (tokens), igual ao Afrodite
    return {k: v for k, v in data.items() if isinstance(v, list) and len(v) > 0}
