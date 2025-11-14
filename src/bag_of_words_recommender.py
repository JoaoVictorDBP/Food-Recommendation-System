from utils import collect_all_ingridients, calculate_ranked_list
import numpy as np


def bag_of_words(data: dict, user_food: list,
                 inverse=False) -> dict:
    all_ingredients = []
    food_vector = {}

    # Armazena todos os ingredientes no array all_ingredients
    all_ingredients = collect_all_ingridients(data)

    for recipe, ingredients in data.items():

        vector_ingredients = np.zeroes(len(all_ingredients))

        # Criando vetor de ingredientes para cada receita
        for ingredient in ingredients:
            idx = all_ingredients.index(ingredient)
            vector_ingredients[idx] = 1

        food_vector[recipe] = vector_ingredients

    # Cria um vetor de usuário
    user_vector = [food_vector[recipe]
                   for recipe in user_food if user_food in food_vector]

    # Calcula a média entre os valores das receitas escolhidas pelo usuário
    profile_mean = np.mean(user_vector, axis=0)

    # Calcula e retorna uma lista ranqueada
    ranked_list = calculate_ranked_list(food_vector, user_food,
                                        profile_mean, inverse)

    # Calcular os top 4
    # Top 4 recomendações
    k = 4
    top_recipes = {}
    counter = 0

    for recipes, similarity in ranked_list.items():
        if counter == k:
            break

        top_recipes[recipes] = similarity

    return top_recipes
