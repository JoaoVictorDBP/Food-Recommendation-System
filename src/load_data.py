# Bibliotecas utilizadas
import json
import pandas as pd
from pathlib import Path

# Função que carrega o arquivo Afrodite.json e extrai
# as informações relevantes (nome, ingredientes e modo de preparo)
#
# Parâmetros:
#   path (str, opcional): caminho para o arquivo JSON. Caso não seja informado,
#                         a função buscará automaticamente na pasta "data"
# Retorno:
#   DataFrame com as colunas: prato, ingredientes, modo_preparo e outras_infos
def load_afrodite(path: str = None) -> pd.DataFrame:
    
    # Define o caminho base do projeto (nível acima deste arquivo)
    base_path = Path(__file__).resolve().parents[1]
    if path is None:
        # Caminho padrão do arquivo afrodite.json
        path = base_path / "data" / "afrodite.json"

    # Abre o arquivo JSON e carrega seu conteúdo
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    registros = []  # Lista para armazenar os pratos processados

    # Percorre cada item (receita) dentro do JSON
    for item in data:
        # Ignora entradas que não sejam dicionários
        if not isinstance(item, dict):
            continue
        
        # Obtém o nome do prato (campo "titulo" ou "nome")
        prato = item.get("titulo") or item.get("nome")

        # Inicializa listas para armazenar informações separadas
        ingredientes, preparo, extras = [], [], []

        # Percorre as seções da receita (ingredientes, preparo etc.)
        for secao in item.get("secao", []):
            nome_secao = secao.get("nome", "").strip().lower()
            conteudo = [c.strip() for c in secao.get("conteudo", []) if c.strip()]
            
            # Classifica o conteúdo conforme o tipo da seção
            if "ingrediente" in nome_secao:
                ingredientes.extend(conteudo)
            elif "preparo" in nome_secao:
                preparo.extend(conteudo)
            else:
                extras.extend(conteudo)

        # Armazena as informações coletadas no formato de dicionário
        registros.append({
            "prato": prato,
            "ingredientes": ingredientes,
            "modo_preparo": preparo,
            "outras_infos": extras
        })

    # Converte a lista de dicionários em um DataFrame
    df = pd.DataFrame(registros)
    return df

# Bloco de teste — executado apenas se o script for chamado diretamente
if __name__ == "__main__":
    df = load_afrodite()
    print(df.head())                     # Mostra as primeiras receitas
    print(f"Total de receitas: {len(df)}")  # Exibe o número total de pratos
