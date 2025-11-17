# aplicação para recomendação de alimentos
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import streamlit as st

from load_data import load_scraping
from preprocessing import preprocess_scraped_ingredients, make_scraping_text_data
from tf_idf_recommender import tf_idf_recommendation

# Função para tentar localizar pratos
def match_receita(nome, data):
    nome = nome.lower().strip()

    # match exato
    if nome in data:
        return nome

    # match parcial
    for k in data:
        if nome in k:
            return k

    return None

# Carregando dados para recomendação
@st.cache_data(show_spinner=True)
def carregar_dados():
    data = load_scraping()
    data = preprocess_scraped_ingredients(data)
    data = make_scraping_text_data(data)
    data = {k: v for k, v in data.items() if len(v) > 0}
    return data

data = carregar_dados()


st.title("Recomendando pratos que você ama (ou odeia) 😋😖")

prato_favorito = st.text_input("Me diga seu prato favorito:")


if st.button("Gerar Recomendação"):

    # Verifica se o usuário digitou algo
    if prato_favorito is None or prato_favorito.strip() == "":
        st.warning("Por favor, digite um prato.")
        st.stop()

    # Tenta localizar a receita na base
    prato_escolhido = match_receita(prato_favorito, data)

    # Se não encontrou, avisa que não está na base
    if prato_escolhido is None:
        st.warning("Prato não encontrado na base, tente outro.")
        st.stop()

    # Normaliza o nome encontrado
    prato_escolhido = prato_escolhido.lower().strip()

    # Executa recomendações (positiva e negativa)
    gif_placeholder = st.empty()
    result_placeholder = st.empty()

    gif_placeholder.markdown("""
        <div style="text-align:center">
            <img src="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExaGEzdWh4aDB3eG82dWc4bDZ4cmlkdHBrY203M2UwemV5bHd4MDN6eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/p0dFF6nzn1DZKKyNdo/giphy.gif" width="180">
            <p style="font-size:20px;">Cozinhando suas recomendações...</p>
        </div>
    """, unsafe_allow_html=True)

    recomendados = tf_idf_recommendation(data, [prato_escolhido])
    n_recomendados = tf_idf_recommendation(data, [prato_escolhido], inverse=True)

    gif_placeholder.empty()

    with result_placeholder.container():
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Você também pode gostar de:")
            for r in recomendados:
                st.write("- " + r)

        with col2:
            st.subheader("Você provavelmente não vai gostar de:")
            for r in n_recomendados:
                st.write("- " + r)