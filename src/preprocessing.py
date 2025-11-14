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

# Função que aplica a limpeza em todos os ingredientes da base
# e cria um texto consolidado com todos os dados relevantes.
#
# Parâmetros:
#   df (DataFrame): base de dados com colunas de ingredientes e preparo
# Retorno:
#   DataFrame com colunas adicionais 'ingredientes_limpos' e 'texto_completo'
def preprocess_ingredients(df: pd.DataFrame) -> pd.DataFrame:
    
    # Cria uma nova coluna com os ingredientes limpos
    df["ingredientes_limpos"] = df["ingredientes"].apply(
        lambda lista: [clean_ingredient(i) for i in lista if isinstance(i, str) and i.strip()]
    )

    # Cria uma coluna 'texto_completo' unindo ingredientes, preparo e outras informações
    df["texto_completo"] = df.apply(
        lambda row: " ".join(
            row.get("ingredientes_limpos", []) +
            row.get("modo_preparo", []) +
            row.get("outras_infos", [])
        ).strip(),
        axis=1
    )

    return df

# Converte o DataFrame em um dicionário {nome_prato: [lista_ingredientes_limpos]}
#
# Parâmetros:
#   df (DataFrame): base já pré-processada
# Retorno:
#   dicionário de pratos e respectivos ingredientes limpos
def make_text_data(df: pd.DataFrame) -> dict:
    return dict(zip(df["prato"], df["ingredientes_limpos"]))

# Bloco de teste — executado apenas se o script for chamado diretamente
if __name__ == "__main__":
    from load_data import load_afrodite  # Importa a função de carregamento
    df = load_afrodite()                 # Carrega os dados brutos
    df = preprocess_ingredients(df)      # Aplica o pré-processamento
    data = make_text_data(df)            # Cria o dicionário final

    # Mostra alguns exemplos de saída
    for k, v in list(data.items())[:3]:
        print(f"\n{k}:\n{v[:200]}...")
