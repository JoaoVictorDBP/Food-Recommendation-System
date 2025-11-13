import numpy
from utils import collect_all_ingridients


# Função que constroi um grafo bipartido (Pratos e ingredientes)
def build_bipartid_graph(data: dict) -> dict:
    bipartid_graph = data.copy()

    # Coleta todos os ingredientes
    all_ingredients = collect_all_ingridients(data)

    # Loop para construir o grafo bipartido
    for ingredient in all_ingredients:
        tmp = []
        for key, value in data.items():
            if ingredient in value:
                tmp.append(key)

        bipartid_graph[ingredient] = tmp

    return bipartid_graph
