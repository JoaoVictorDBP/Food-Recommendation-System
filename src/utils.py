import numpy as np


def tf_idf(data):
    tf_idf_dict = {}
    all_ingredients = []

    for key, value in data.items():
        for ingredients in value:
            all_ingredients.append(ingredients)

    all_ingredients = np.sort(np.unique(all_ingredients))

    for key, value in data.items():
        ingredients_vector = np.zeros(len(all_ingredients))
        tf_value = tf(value)

        for ingredient in value:
            tf_idf_res = tf_value*idf(data, ingredient)
            idx = all_ingredients.index(ingredient)
            ingredients_vector[idx] = tf_idf_res

        tf_idf_dict[key] = ingredients_vector

    return tf_idf_dict


def tf(ingredient_list):
    n_ingredients = len(ingredient_list)

    return 1/n_ingredients


def idf(data, t):
    n = len(data)
    nt = 0

    for key, value in data.items():
        for ingredient in value:
            if (ingredient == t):
                nt += 1
                break

    idf_res = np.log10(n/nt)

    return idf_res


def cosine_sim(A, B):

    norm_A = np.linalg.norm(A)
    norm_B = np.linalg.norm(B)

    cosine_sim = np.dot(A, B)/(norm_A*norm_B)

    return cosine_sim


def jaccard_sim(A, B):

    set_A = set(A)
    set_B = set(B)

    intersection = len(set_A.intersection(set_B))
    union = len(set_A.union(set_B))

    return intersection / union


def mean_profile_recommendation(data, user_food):
    food_vector = tf_idf(data)

    user_vector = [food_vector[dish]
                   for dish in user_food if user_food in food_vector]

    profile_mean = np.mean(user_vector, axis=0)

    sim = {}

    for key, value in food_vector.items():
        if key in user_food:
            continue

    cos_sim = cosine_sim(profile_mean, value)
    sim[key] = cos_sim

    sorted_recommendation = sorted(
        sim.items(), key=lambda item: item[1], reverse=True)

    return sorted_recommendation
