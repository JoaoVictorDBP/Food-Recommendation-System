# arquivo de testes para auxiliar na real implementação

import streamlit as st
import pandas as pd
import numpy as np

prato = st.text_input("Digite seu prato preferido:")

if st.button("Recomendar"):
    st.write(f"Voce escolheu: {prato}")
    st.write("Recomendados: Prato A, Prato B, Prato C")

df = pd.DataFrame({'first column': [1, 2, 3], 'second column': [4, 5, 6]})
df

st.line_chart(df)

x = st.slider('x')
st.write(x, "ao quadrado eh" ,x*x)

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)

# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)


left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
left_column.button('Press me!')

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")