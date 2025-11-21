import re

# LIMPEZA DE INGREDIENTES

def clean_ingredient(ing: str) -> str:
    """
    Normaliza e limpa uma string de ingrediente, removendo ruídos
    e padronizando termos culinários.

    A limpeza inclui:
      • conversão para minúsculas
      • remoção de números e unidades de medida
      • remoção de descritores culinários (picado, fatiado, etc.)
      • remoção de símbolos
      • normalização de expressões equivalentes (ex: chocolate ao leite → chocolate)

    Parâmetros:
        ing (str): Ingrediente bruto coletado do scraping.

    Retorno:
        str: Ingrediente limpo e normalizado.
    """

    ing = ing.lower()

    # Remove números e unidades
    ing = re.sub(r"\b\d+[.,]?\d*\b", " ", ing)
    ing = re.sub(
        r"\b(ml|g|kg|mg|litro|xícara|xicara|colher|colheres|lata|latas|"
        r"unidade|unidades|pacote|pacotes|gramas?)\b",
        " ",
        ing,
    )

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

    # Símbolos e espaços
    ing = re.sub(r"[^a-zA-Zà-ÿ\s]", " ", ing)
    ing = re.sub(r"\s+", " ", ing).strip()

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
        "suco de gengibre": "gengibre",
    }

    for k, v in NORMALIZATION_MAP.items():
        if ing == k or ing.startswith(k):
            ing = v

    ing = re.sub(r"^de\s+|\s+de$", "", ing).strip()
    ing = re.sub(r"\s+", " ", ing)

    return ing


def normalize_title(title: str) -> str:
    """
    Limpa e padroniza o título de uma receita.

    A padronização remove:
      • parênteses e conteúdos internos
      • números irrelevantes (ex.: versões)
      • termos redundantes (simples, rápido, microondas, etc.)

    Parâmetros:
        title (str): Nome original da receita.

    Retorno:
        str: Nome normalizado.
    """

    title = title.lower()

    # remove parenteses
    title = re.sub(r"\(.*?\)", " ", title)

    # remove números que criam variações inúteis
    title = re.sub(r"\b\d+\b", " ", title)

    REPLACE = {
        "microondas": "",
        "de microondas": "",
        "na caneca": "caneca",
        "de caneca": "caneca",
        "caneca de": "caneca",
        "simples": "",
        "fácil": "",
        "rapido": "",
        "rápido": "",
    }

    for k, v in REPLACE.items():
        title = title.replace(k, v)

    title = re.sub(r"\s+", " ", title).strip()
    return title


def deduplicate_by_ingredients(data: dict, threshold=0.80) -> dict:
    """
    Remove receitas duplicadas ou quase duplicadas analisando
    a similaridade entre listas de ingredientes.

    Similaridade usada: Jaccard manual
        sim = |interseção| / |união|

    Se sim >= threshold, considera-se duplicata.

    Parâmetros:
        data (dict): Base no formato {prato: [ingredientes]}
        threshold (float): Limite de duplicação.

    Retorno:
        dict: Base limpa de receitas repetidas.
    """

    clean_data = {}
    seen = []

    for prato, ingredientes in data.items():
        is_duplicate = False

        for saved_name, saved_ingredients in seen:
            inter = len(set(ingredientes) & set(saved_ingredients))
            uni = len(set(ingredientes) | set(saved_ingredients))
            sim = inter / uni

            if sim >= threshold:
                is_duplicate = True
                break

        if not is_duplicate:
            clean_data[prato] = ingredientes
            seen.append((prato, ingredientes))

    return clean_data


def preprocess_scraped_ingredients(raw_data: dict) -> dict:
    """
    Executa toda a pipeline de limpeza dos dados brutos de scraping.

    Etapas:
      1. Normaliza o título da receita.
      2. Limpa todos os ingredientes.
      3. Remove duplicatas de ingredientes.
      4. Remove receitas com poucos ingredientes.
      5. Remove receitas duplicadas entre si.

    Parâmetros:
        raw_data (dict): Base crua do scraping.

    Retorno:
        dict: Base final processada.
    """

    processed = {}

    for prato, ingredientes in raw_data.items():
        receita = normalize_title(prato)
        limpos = []

        for ing in ingredientes:
            if isinstance(ing, str) and ing.strip():
                limpos.append(clean_ingredient(ing))

        limpos = sorted(list(set(limpos)))

        if len(limpos) >= 3:  # remove receitas lixo
            processed[receita] = limpos

    processed = deduplicate_by_ingredients(processed)
    return processed


def make_scraping_text_data(data: dict) -> dict:
    """
    Remove receitas que ficaram com lista de ingredientes vazia
    após o preprocessamento.

    Parâmetros:
        data (dict): Base pré-processada.

    Retorno:
        dict: Base filtrada apenas com receitas válidas.
    """

    return {k: v for k, v in data.items() if len(v) > 0}
