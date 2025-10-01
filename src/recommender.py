# sistema de recomendação de alimentos

# recommender.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity

# Exemplo de dataset pequeno
data = {
    "nome": ["Feijoada", "Macarrão à bolonhesa", "Strogonoff de frango"],
    "ingredientes": [
        ["feijão preto", "carne seca", "linguiça", "arroz", "couve"],
        ["macarrão", "carne moída", "molho de tomate", "cebola", "alho"],
        ["frango", "creme de leite", "ketchup", "arroz", "batata palha"]
    ]
}
df = pd.DataFrame(data)

# One-hot encoding dos ingredientes
mlb = MultiLabelBinarizer()
X = mlb.fit_transform(df["ingredientes"])

# Similaridade entre pratos
sim_matrix = cosine_similarity(X)

def recomendar(prato, topn=2):
    """Recomenda pratos similares a partir de um prato informado"""
    idx = df[df["nome"] == prato].index[0]
    scores = list(enumerate(sim_matrix[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    recomendados = [df.iloc[i]["nome"] for i, _ in scores[1:topn+1]]
    return recomendados

def get_pratos():
    """Retorna a lista de pratos disponíveis"""
    return df["nome"].tolist()