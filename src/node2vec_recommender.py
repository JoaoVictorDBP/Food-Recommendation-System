import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def get_graph_recommendations(prato_nome, embeddings):

    # Verifica se o prato está nos embeddings
    if prato_nome not in embeddings:
        return []

    target_vec = np.array(embeddings[prato_nome]).reshape(1, -1)

    # Preparar matrizes para cálculo vetorizado
    candidatos = []
    vetores_candidatos = []

    for nome, vetor in embeddings.items():
        if nome != prato_nome:
            candidatos.append(nome)
            vetores_candidatos.append(vetor)

    if not candidatos:
        return []

    # Aqui é usado a similaridade de cossenos do sklearn
    sim_matrix = cosine_similarity(target_vec, vetores_candidatos)

    # Ordenação dos índices baseada no score (do maior para o menor)
    sorted_indices = np.argsort(sim_matrix[0])[::-1]

    recomendacoes = []
    for idx in sorted_indices:
        recomendacoes.append(candidatos[idx])

    return recomendacoes
