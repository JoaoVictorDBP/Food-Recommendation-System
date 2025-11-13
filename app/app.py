# aplicação para recomendação de alimentos

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import streamlit as st

from load_data import load_afrodite
from preprocessing import preprocess_ingredients, make_text_data
from tf_idf_recommender import tf_idf_recommendation
from graph_recommender import build_bipartid_graph

# Carregando e processando os dados
@st.cache_data(show_spinner=True)
def carregar_dados():
    df = load_afrodite()
    df = preprocess_ingredients(df)
    data = make_text_data(df)
    data = {k: v for k, v in data.items() if len(v) > 0}
    return data

data = carregar_dados()

st.title("Recomendando pratos que você ama (ou odeia) 😋😖")

prato_favorito = st.text_input("Me diga seu prato favorito:")

if st.button("Gerar Recomendação"):

    if prato_favorito not in data:
        st.warning("Prato não encontrado na base, tente outro.")
    else:

        # placeholders criados
        gif_placeholder = st.empty()
        result_placeholder = st.empty()

        # Apaga resultados anteriores
        result_placeholder.empty()

        # GIF
        gif_placeholder.markdown("""
            <div style="text-align:center">
                <img src="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExaGEzdWh4aDB3eG82dWc4bDZ4cmlkdHBrY203M2UwemV5bHd4MDN6eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/p0dFF6nzn1DZKKyNdo/giphy.gif" width="180">
                <p style="font-size:20px;">Cozinhando suas recomendações...</p>
            </div>
        """, unsafe_allow_html=True)

        # Calcula recomendações
        recomendados = tf_idf_recommendation(data, [prato_favorito])
        n_recomendados = tf_idf_recommendation(data, [prato_favorito])

        # Remove GIF
        gif_placeholder.empty()

        # Exibe resultados
        with result_placeholder.container():
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Você também pode gostar de:")
                for r in recomendados:
                    st.write(f"- {r}")

            with col2:
                st.subheader("Você provavelmente não vai gostar de:")
                for r in n_recomendados:
                    st.write(f"- {r}")
