import sys
import os
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "src")))

import streamlit as st

from tf_idf_recommender import tf_idf_recommendation
from preprocessing import preprocess_scraped_ingredients, make_scraping_text_data
from load_data import load_scraping
from node2vec_recommender import get_graph_recommendations
import pickle


def match_receita(nome, data):
    """
    Tenta localizar na base a receita cujo nome corresponde ao texto digitado
    pelo usuário.

    Métodos utilizados:
      • Match exato  → retorna a receita se o nome for idêntico.
      • Match parcial → retorna a primeira receita cujo nome contenha a string.

    Parâmetros:
        nome (str): Texto digitado pelo usuário.
        data (dict): Base de receitas já pré-processada.

    Retorno:
        str | None: Nome da receita encontrada ou None se nenhuma combinar.
    """
    nome = nome.lower().strip()

    if nome in data:
        return nome

    for k in data:
        if nome in k:
            return k

    return None



@st.cache_data(show_spinner=True)
def carregar_dados():
    """
    Carrega os dados brutos do scraping, aplica toda a pipeline de
    preprocessamento e retorna a base pronta para uso do TF-IDF.

    Etapas:
      1. load_scraping() → carrega receitas cruas.
      2. preprocess_scraped_ingredients() → normaliza títulos e limpa ingredientes.
      3. make_scraping_text_data() → remove receitas vazias.

    Retorno:
        dict: Base final no formato {nome_receita: [lista_ingredientes]}
    """
    raw = load_scraping()
    data = preprocess_scraped_ingredients(raw)
    data = make_scraping_text_data(data)
    return data

#Carrega valores de embeddings
@st.cache_resource
def carregar_embeddings():
    try:
        with open("graph_embeddings.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

data = carregar_dados()
embeddings = carregar_embeddings()

st.title("Recomendando pratos que você ama (ou odeia) 😋😖")

# Input do usuário contendo o prato favorito
prato_favorito = st.text_input("Me diga seu prato favorito:")


if st.button("Gerar Recomendação"):

    # Valida input vazio
    if not prato_favorito.strip():
        st.warning("Por favor, digite um prato.")
        st.stop()

    # Tenta encontrar o prato dentro da base
    prato_escolhido = match_receita(prato_favorito, data)

    if prato_escolhido is None:
        st.warning("Prato não encontrado na base, tente outro.")
        st.stop()

    prato_escolhido = prato_escolhido.lower().strip()

    # Espaços para exibir GIF de processamento e o resultado final
    gif_placeholder = st.empty()
    result_placeholder = st.empty()

    # Exibe animação enquanto calcula recomendações
    gif_placeholder.markdown("""
        <div style="text-align:center">
            <img src="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExaGEzdWh4aDB3eG82dWc4bDZ4cmlkdHBrY203M2UwemV5bHd4MDN6eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/p0dFF6nzn1DZKKyNdo/giphy.gif" width="180">
            <p style="font-size:20px;">Cozinhando suas recomendações...</p>
        </div>
    """, unsafe_allow_html=True)

    # Executa o motor de recomendação baseado em TF-IDF
    # Retorna uma lista ordenada de pratos semelhantes ao escolhido
    pratos_embeddings = get_graph_recommendations(prato_escolhido, embeddings)
    todos_pratos = list(tf_idf_recommendation(data, [prato_escolhido]).keys())

    # Remove recomendações que contenham literalmente a string digitada
    # Isso evita sugerir o próprio prato ou variantes de nome
    query = prato_favorito.lower().strip()
    pratos_embeddings = [p for p in pratos_embeddings if query not in p]

    # Seleciona 4 mais parecidos e 4 menos parecidos
    k = 4
    recomendados = pratos_embeddings[:k]
    n_recomendados = todos_pratos[::-1][:k]

    gif_placeholder.empty()

    # Exibe resultados
    with result_placeholder.container():
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Você também pode gostar de:")
            for r in recomendados:
                st.write("- " + r)

        with col2:
            st.subheader("Tente explorar novos pratos:")
            for r in n_recomendados:
                st.write("- " + r)
