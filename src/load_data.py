import json
import pandas as pd
from pathlib import Path

def load_afrodite(path: str = None) -> pd.DataFrame:
    """Carrega o arquivo Afrodite.json e extrai nome das receitas e ingredientes."""
    base_path = Path(__file__).resolve().parents[1]
    if path is None:
        path = base_path / "data" / "afrodite.json"

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    registros = []
    for item in data:
        if not isinstance(item, dict):
            continue
        
        prato = item.get("titulo") or item.get("nome")
        ingredientes = []

        # procura por qualquer seção cujo nome contenha "ingrediente"
        for secao in item.get("secao", []):
            nome_secao = secao.get("nome", "").strip().lower()
            if "ingrediente" in nome_secao:
                # remove strings vazias e espaços extras
                ingredientes = [i.strip() for i in secao.get("conteudo", []) if i.strip()]
                break

        # adiciona também pratos sem ingredientes definidos
        registros.append({
            "prato": prato,
            "ingredientes": ingredientes
        })

    df = pd.DataFrame(registros)
    return df

if __name__ == "__main__":
    df = load_afrodite()
    print(df.head())
    print(f"Total de receitas: {len(df)}")
