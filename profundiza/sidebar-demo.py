import streamlit as st

# Crear el título de la aplicación web
st.title("Mi primera Aplicación Web con Streamlit")
sidebar = st.sidebar
sidebar.title("Esta es una barra lateral")
sidebar.write("Aquí van los elementos de entrada")

st.header("Información sobre el conjunto de datos")
st.header("Descripción de los datos")
st.write("""
         Este es un ejemplo simple de una app para predecir.
         
         ¡Esta app predice mis datos!
""")
         
