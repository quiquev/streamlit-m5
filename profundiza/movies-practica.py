import pandas as pd
import streamlit as st

DATA_URL = "movies.csv"
BUFF_SIZE = 500
#df = pd.read_csv(DATA_URL)

@st.cache
def load_data(rows, searchFilmInput, searchDirFilm):
    data = pd.read_csv(DATA_URL, nrows=rows)
    if (searchFilmInput):
        data = data[data["name"].str.upper().str.contains(searchFilmInput.upper())]
    if (searchDirFilm):
        data = data[data["director"].str.contains(searchDirFilm)]
    return data

load_state = st.text("Cargando datos...")
df = load_data(BUFF_SIZE, "", "")
load_state.text("Carga completada.")


# Sidebar controls
sidebar = st.sidebar
sidebar.title("Filtros")

# Filtro checkbox
showData = sidebar.checkbox("¿Mostrar datos?")
if showData:
    st.dataframe(df, use_container_width=True)
sidebar.markdown("---")

# Filtro búsqueda
searchFilmInput = sidebar.text_input("Introduce el film a buscar")
searchFilmButton = sidebar.button("Buscar film")
if (searchFilmButton):
    filtered_df = load_data(BUFF_SIZE, searchFilmInput, "")
    st.dataframe(filtered_df, use_container_width=True)   # actualiza el DF filtrado
sidebar.markdown("---")

# Filtro SelectBox
directorSelected = sidebar.selectbox("Seleccionar un Director", df["director"].unique(), index=0)
searchDirButton = sidebar.button("Buscar director")
if (searchDirButton):
    filtered_df = load_data(BUFF_SIZE, "", directorSelected)
    st.dataframe(filtered_df, use_container_width=True)   # actualiza el DF filtrado