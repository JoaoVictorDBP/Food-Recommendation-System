from load_data import load_afrodite
from preprocessing import preprocess_ingredients, make_text_data
from tf_idf_recommender import tf_idf_recommendation
from graph_recommender import build_bipartid_graph

# Careggando e processando os dados
df = load_afrodite()
df = preprocess_ingredients(df)
data = make_text_data(df)
data = {k: v for k, v in data.items() if len(v) > 0}

# Prato para simular funcionamento
user_food = ["Alfajor de leite"]

# Gerando recomendações
print(f"Escolha do usuário: {user_food}")
recs = tf_idf_recommendation(data, user_food)
print("\nRecomendações:")
for prato, score in recs.items():
    print(f"{prato}: {score:.4f}")

print(build_bipartid_graph(data))
