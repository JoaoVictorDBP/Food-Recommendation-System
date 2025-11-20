# Bibliotecas utilizadas
import numpy as np
import sys


# Aplica o algoritmo tf-idf na base de dados
# O algoritmo associa as receitas aos seus repsectivos
# vetores construidos utilizando o algoritmo tf-idf
#
# Parâmetros: Base de dados (dict)
# Retorno: Dicionário com as receitas e os vetores tf-idf
def tf_idf(data: dict) -> dict:
    tf_idf_dict = {}
    all_ingredients = []

    # Armazena todos os ingredientes no array all_ingredients
    all_ingredients = collect_all_ingridients(data)

    for key, value in data.items():
        # Cria o vetor dos ingredientes (inicializados com zero)
        ingredients_vector = np.zeros(len(all_ingredients))
        # Aplica o tf
        tf_value = tf(value)

        # Constroi o vetor de frequência dos ingredientes para cada receita
        for ingredient in value:
            tf_idf_res = tf_value*idf(data, ingredient)
            idx = all_ingredients.index(ingredient)
            ingredients_vector[idx] = tf_idf_res

        # Associa uma receita ao seu vetor de ingredientes
        tf_idf_dict[key] = ingredients_vector

    return tf_idf_dict


# Calcula a frequência de um termo dentro do vetor de ingredientes
#
# Parâmetros: lista de ingredientes
# Retorno: frequência
def tf(ingredient_list: list) -> float:
    n_ingredients = len(ingredient_list)

    return 1/n_ingredients


# Calcula o frquência inversa do documento (idf)
#
# Parâmetros: Base de dados, termo
# Retorno: resultado do idf
def idf(data: dict, t: str) -> float:
    n = len(data)
    nt = 0

    for key, value in data.items():
        for ingredient in value:
            if (ingredient == t):
                nt += 1
                break

    idf_res = np.log10(n/nt)

    return idf_res


# Calcula a similaridade de cossenos
#
# Parâmetros: Vetores A e B
# Retorno: Valor da similaridade
def cosine_sim(A: list, B: list) -> float:

    norm_A = np.linalg.norm(A)
    norm_B = np.linalg.norm(B)

    cosine_sim = np.dot(A, B)/(norm_A*norm_B)

    return cosine_sim


# Calcula a similaridade de jaccard
#
# Parâmetros: Vetores A e B
# Retorno: Valor da similaridade
def jaccard_sim(A: list, B: list) -> float:

    set_A = set(A)
    set_B = set(B)

    intersection = len(set_A.intersection(set_B))
    union = len(set_A.union(set_B))

    return intersection / union


# Função que obtem todos os ingredientes e armazena em um array
#
# Parâmetros: base de dados
# Retorno: lista dos ingredientes
def collect_all_ingridients(data: dict) -> list:
    all_ingredients = []

    for key, value in data.items():
        for ingredients in value:
            all_ingredients.append(ingredients)

    # Caso não haja dados suficientes, sai do programa
    if (len(all_ingredients) < 2):
        print("Não há dados suficientes para executar o algoritmo")
        sys.exit(0)

    # Ordena o array e remove duplicatas
    all_ingredients = sorted(list(set(all_ingredients)))

    return all_ingredients


def calculate_ranked_list(food_vector: list, user_food: list,
                          profile_mean: list) -> dict:
    sim = {}

    # Aplica similaridade de cossenos entre o vetor de usuário e
    # os pratos da base de dados
    for recipe, vector in food_vector.items():
        if recipe in user_food:
            continue
        cos_sim = cosine_sim(profile_mean, vector)
        sim[recipe] = cos_sim

    # Caso normal → ordena do mais parecido para o menos parecido

    sorted_recommendation = sorted(
        sim.items(), key=lambda item: item[1], reverse=True
    )

    return dict(sorted_recommendation)
