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
    ing = ing.lower()  # Converte para minúsculas

    # Remove quantidades e unidades de medida comuns (ex: "2 colheres", "100g", "1 xícara")
    ing = re.sub(r"\d+[.,]?\d*|\b(ml|g|kg|xícara|colher|colheres|unidade|unidades|pedaço|litro|l)\b", "", ing)

    # Remove caracteres especiais e mantém apenas letras e espaços
    ing = re.sub(r"[^a-zA-ZÀ-ÿ\s]", "", ing)

    # Remove espaços extras e palavras "de" isoladas no início ou final
    ing = ing.strip()
    ing = re.sub(r"^de\s+|\s+de$", "", ing)
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
