import pickle
import networkx as nx
from node2vec import Node2Vec
from app import carregar_dados  # Importando sua função de carregar dados existente


def treinar_e_salvar_embeddings():
    print("1. Carregando dados...")
    # Nota: O Streamlit pode reclamar se rodar a função cacheada fora do app.
    # Se der erro, copie a lógica interna de 'carregar_dados' para cá.
    data = carregar_dados()

    print("2. Construindo Grafo...")
    G = nx.DiGraph(data)

    print(f"   - Nós: {G.number_of_nodes()}")
    print(f"   - Arestas: {G.number_of_edges()}")

    print("3. Treinando Node2Vec (Isso pode demorar)...")
    # Aumentei um pouco os parâmetros para melhor qualidade, já que é offline
    node2vec = Node2Vec(G, dimensions=64, walk_length=40,
                        num_walks=80, workers=4, quiet=False)

    model = node2vec.fit(window=10, min_count=1, batch_words=4)

    # 4. Extraindo apenas o dicionário de vetores (mais leve que salvar o modelo todo)
    print("4. Salvando embeddings em arquivo pickle...")
    embeddings = {str(node): model.wv[str(node)] for node in G.nodes()}

    with open("graph_embeddings.pkl", "wb") as f:
        pickle.dump(embeddings, f)

    print("Concluído! Arquivo 'graph_embeddings.pkl' gerado.")


if __name__ == "__main__":
    treinar_e_salvar_embeddings()
