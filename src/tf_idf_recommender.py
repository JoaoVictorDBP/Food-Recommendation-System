from utils import tf_idf, calculate_ranked_list
import numpy as np


# RECOMENDADOR USANDO TF-IDF
# Utiliza o algoritmo tf-idf e similaridade de cossenos
# para gerar um ranking dos pratos recomendados para o usuário
#
#
# Parâmetros: Base de dados, pratos escolhidos pelo user
def tf_idf_recommendation(data: dict, user_food: list) -> dict:

    # Usa o algoritmo tf-idf para o embedding das receitas
    food_vector = tf_idf(data)

    # Cria um vetor de usuário
    user_vector = [food_vector[recipe]
                   for recipe in user_food if user_food in food_vector]

    # Calcula a média entre os valores das receitas escolhidas pelo usuário
    profile_mean = np.mean(user_vector, axis=0)

    ranked_list = calculate_ranked_list(
        food_vector, user_food, profile_mean)

    # Top 4 recomendações
    k = 4
    top_recipes = {}
    counter = 0

    for recipes, similarity in ranked_list.items():
        if counter == k:
            break

        top_recipes[recipes] = similarity

    return top_recipes
