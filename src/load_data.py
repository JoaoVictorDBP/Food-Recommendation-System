# Bibliotecas utilizadas
import json
import pandas as pd
from pathlib import Path

# Carrega os dados obtidos com o scrapping
def load_scraping():
    base_path = Path(__file__).resolve().parents[1]
    path = base_path / "data" / "receitas.json"

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data  # formato: {prato: [ingredientes]}
