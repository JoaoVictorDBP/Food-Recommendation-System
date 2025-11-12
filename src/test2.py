from load_data import load_afrodite
from preprocessing import preprocess_ingredients, make_text_data
from tf_idf_recommender import tf_idf_recommendation

# Careggando e processando os dados
df = load_afrodite()
df = preprocess_ingredients(df)
data = make_text_data(df)
data = {k: v for k, v in data.items() if len(v) > 0}

# Prato para simular funcionamento
user_food = ["Brownie de Chocolate com Gengibre"]

# Gerando recomendações
recs = tf_idf_recommendation(data, user_food)
print("\nRecomendações:")
for prato, score in recs.items():
    print(f"{prato}: {score:.4f}")