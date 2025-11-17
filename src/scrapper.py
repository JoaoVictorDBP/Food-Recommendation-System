import requests
from bs4 import BeautifulSoup
import time
import json
import os
import unicodedata


BASE_URL = "https://cybercook.com.br"
RECIPE_LIST_URL = "https://cybercook.com.br/receitas?pagina={}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

dados = {}  # {nome_prato: [ingredientes]}

# Caminho do arquivo JSON relativo ao projeto
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))      # Projeto/src
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data")            # Projeto/data
JSON_PATH = os.path.join(DATA_DIR, "receitas.json")          # Projeto/data/receitas.json


# cria a pasta data se não existir
os.makedirs(DATA_DIR, exist_ok=True)


# Normalização e deduplicação
def normalizar(ingrediente: str) -> str:
    ing = ingrediente.strip().lower()
    ing = ''.join(
        c for c in unicodedata.normalize('NFD', ing)
        if unicodedata.category(c) != 'Mn'
    )
    return ing


def padronizar_lista(ingredientes):
    vistos = set()
    resultado = []

    for ing in ingredientes:
        norm = normalizar(ing)

        if norm not in vistos:
            vistos.add(norm)
            resultado.append(norm)

    return resultado


# Coletar links das receitas em uma página
def coletar_links(pagina):
    url = RECIPE_LIST_URL.format(pagina)
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")

    links_raw = soup.select("a[href^='/receitas/']")

    receitas_set = set()  # evita duplicatas

    for link in links_raw:
        href = link.get("href")

        if href and href.split("-")[-1].isdigit():
            receitas_set.add(BASE_URL + href)

    # retorna lista já sem duplicatas
    return list(receitas_set)


# Extrair nome e ingredientes de uma receita
def extrair_receita(url):
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")

    titulo = soup.find("h1").get_text(strip=True)

    ingredientes_raw = soup.select("p.font-normal")

    ingredientes = []
    for p in ingredientes_raw:
        bold = p.find("b")
        if bold:
            ingredientes.append(bold.get_text(strip=True))

    # aplica padronização dos itens
    ingredientes = padronizar_lista(ingredientes)

    return titulo, ingredientes


# Loop principal
todos_links = []

print("Coletando links...")

for pg in range(1, 51): 
    print(f"Página {pg}...")
    links = coletar_links(pg)
    todos_links.extend(links)
    time.sleep(1)

print(f"Total de links coletados: {len(todos_links)}")


# ---------------------------------------------------------
# Extrair cada receita
# ---------------------------------------------------------
print("Extraindo receitas...")

for i, link in enumerate(todos_links):
    print(f"[{i+1}/{len(todos_links)}] {link}")
    titulo, ingredientes = extrair_receita(link)

    if titulo and ingredientes:
        dados[titulo] = ingredientes

    time.sleep(0.5)


# Salvar no JSON final
with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=4)

print(f"\nArquivo salvo em: {JSON_PATH}")
print("Scraping concluído!")
