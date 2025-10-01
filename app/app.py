# aplicação para recomendação de alimentos

# app.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from recommender import recomendar, get_pratos

import streamlit as st

st.title("Sistema de Recomendação de Pratos")

# Dropdown para selecionar um prato
prato_favorito = st.text_input("Me diga seu prato favorito:")

if st.button("Recomendar"):
    recomendados = recomendar(prato_favorito)
    st.subheader("Você também pode gostar de:")
    for r in recomendados:
        st.write(f"- {r}")
