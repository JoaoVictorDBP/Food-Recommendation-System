import pandas as pd
import re

def clean_ingredient(ing: str) -> str:
    """Remove quantidades, medidas e caracteres desnecessários e palavras 'de' isoladas."""
    ing = ing.lower()
    # remove números inteiros e decimais + unidades
    ing = re.sub(r"\d+[.,]?\d*|\b(ml|g|kg|xícara|colher|colheres|unidade|unidades|pedaço|litro|l)\b", "", ing)
    # remove caracteres especiais, preservando letras acentuadas
    ing = re.sub(r"[^a-zA-ZÀ-ÿ\s]", "", ing)
    # remove espaços extras
    ing = ing.strip()
    # remove "de" isolado no início ou fim
    ing = re.sub(r"^de\s+|\s+de$", "", ing)
    # remove múltiplos espaços internos
    ing = re.sub(r"\s+", " ", ing)
    return ing


def preprocess_ingredients(df: pd.DataFrame) -> pd.DataFrame:
    """Limpa e normaliza todos os ingredientes do DataFrame."""
    df["ingredientes_limpos"] = df["ingredientes"].apply(
        lambda lista: [clean_ingredient(i) for i in lista if isinstance(i, str) and i.strip()]
    )
    return df

# --- Apenas para teste  ---
if __name__ == "__main__":
    from load_data import load_afrodite  
    df = load_afrodite()
    df = preprocess_ingredients(df)
    print(df.head(10))  # mostra os primeiros 10 pratos com ingredientes limpos