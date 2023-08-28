import streamlit as st
import pandas as pd

DATA_URL = "https://raw.githubusercontent.com/jeaggo/tc3068/master/Superstore.csv"
df = pd.read_csv(DATA_URL)

st.title("Ejercicio Actívate: Sidebar")
st.header("Información de las tiendas de Walmart en Estados Unidos")
st.subheader("Predicción de ventas para la productos de línea blanca.")

sidebar = st.sidebar
sidebar.title("Sección de Filtros")
#sidebar.write("Aquí irán los filtros de la aplicaión")

# Creación de filtros para la app
shipModeSelected = sidebar.radio("Seleccione el Modo de Entrega", df["Ship Mode"].unique())
sidebar.write("Modo seleccionado:", shipModeSelected)
sidebar.markdown("---")

categSelected = sidebar.selectbox("Seleccione una Categoría", df["Category"].unique())
sidebar.write(f"Categoría seleccionada: {categSelected!r}")
sidebar.markdown("---")

discountRange = sidebar.slider("Seleccione un rango de Descuento", min_value=float(df["Discount"].min()), max_value=float(df["Discount"].max()), 
                               value=(float(df["Discount"].min()), float(df["Discount"].max())))
subsetDiscount = df[df["Discount"].between(discountRange[0], discountRange[1])]
sidebar.write(f"Rango de descuento entre: {discountRange}, Total de órdenes: {subsetDiscount.shape[0]} / {df.shape[0]}")