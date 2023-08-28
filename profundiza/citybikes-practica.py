import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

DATA_URL = "citibike-tripdata.csv"
BUFF_SIZE = 500

@st.cache
def load_data(rows):
    data = pd.read_csv(DATA_URL, nrows=rows)
    data["started_at"] = pd.to_datetime(data["started_at"])
    data["ended_at"] = pd.to_datetime(data["ended_at"])
    return data

load_state = st.text("Cargando datos...")
df = load_data(BUFF_SIZE)
load_state.text("Carga completada.")

# Sidebar controls
sidebar = st.sidebar
sidebar.title("Filtros")

# Filtro checkbox
showData = sidebar.checkbox("¿Mostrar datos?")
if showData:
    st.dataframe(df, use_container_width=True)
sidebar.markdown("---")

# Bar chart
work_df = df[["ride_id", "started_at"]]
work_df["started_hour"] = work_df["started_at"].dt.hour
rides_by_hour_df = work_df[["started_hour", "ride_id"]].groupby("started_hour").count()
fig, ax = plt.subplots()
rides_by_hour_df.plot.bar(ax=ax, xlabel="Hora del Día", ylabel="Total Viajes", title="Viajes por Hora", legend=False)
st.pyplot(fig)