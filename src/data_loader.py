# carregar dados e gerar dataframes

import pandas as pd

raw_recipes = pd.read_csv("data/RAW_recipes.csv")
raw_recipes_df = pd.DataFrame(raw_recipes)

print(raw_recipes_df.head())

pp_recipes = pd.read_csv("data/PP_recipes.csv")
pp_recipes_df = pd.DataFrame(pp_recipes)

print(pp_recipes_df.head())
