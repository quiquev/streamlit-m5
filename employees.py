"""
File: employees.py
Author: Luis Enrique Villaseñor Aguilar
Date: August 27, 2023

Description: This is a web application for a Data Science project regarding
analysis of attrition rates. 
- Data Science & AI, 23009P, Tecnologico de Monterrey.

This script is protected by copyright law. Unauthorized copying or
distribution of this script, or any portion of it, may result in severe
civil and criminal penalties. Individuals found in violation of this
notice will be held legally responsible.

Permission is hereby granted to use, modify, and distribute this script
for educational, personal, and non-commercial purposes, provided that
the above copyright notice and this permission notice appear in all
copies of the script.

THIS SCRIPT IS PROVIDED "AS IS," WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR
OTHER LIABILITY ARISING FROM, OUT OF, OR IN CONNECTION WITH THE SCRIPT.

For inquiries or permission requests, please contact:
    luis.enrique.villasenor@gmail.com
"""

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

DATA_URL = "Employees.csv"
BUFF_SIZE = 500

# Cache fuction
@st.cache
def load_data (rows=BUFF_SIZE, employee_id=None, hometown=None, unit=None, educationLvl=None, city=None, unitSb=None):
    data = pd.read_csv(DATA_URL, nrows=rows)
    if (employee_id or hometown or unit or educationLvl):
        # For select boxes default value is validated and set to flags
        flagEducationLvl = isinstance(educationLvl, str)
        flagCity = (city == "Seleccionar..." )
        flagUnitSb = (unitSb == "Seleccionar..." )
        data = data.query("\
                          (@employee_id.__len__() == 0 | Employee_ID.str.contains(@employee_id, case=False)) &\
                          (@hometown.__len__() == 0 | Hometown.str.contains(@hometown, case=False)) & \
                          (@unit.__len__() == 0 | Unit.str.upper() == @unit.upper()) & \
                          (@flagEducationLvl | Education_Level == @educationLvl) & \
                          (@flagCity | Hometown == @city) & \
                          (@flagUnitSb | Unit == @unitSb)")
    return data

# Fetch data
df = load_data(BUFF_SIZE)

# Wrapper for cache function when filters are applied
def filter_df (employee_id=None, hometown=None, unit=None):
    df = load_data(BUFF_SIZE, employee_id, hometown, unit)
    
# Dashboard title, header and subheader
st.title("Análisis de Deserción Laboral")
st.header("Objetivo del Tablero: Analizar el fénomeno de deserción laboral que afecta a empresas y organizaciones en la actualidad.")
st.subheader("*Fuente de los Datos: Hackathon HackerEarth 2020.*")
st.markdown("---")

# Sidebar container
sidebar = st.sidebar
sidebar.title("Filtros de Contenido")

# Show & hide function for DF
def showHideDF (checked=None):
    if checked:
        st.dataframe(df, use_container_width=True)

# Text input filters section; Employee_ID, Hometown, Unit
empIdFilter = sidebar.text_input("Filtrar por número de empleado:", placeholder="Employee ID", help="Presione 'Enter' o el botón 'Buscar' para aplicar filtros de texto")
hometownFilter = sidebar.text_input("Filtrar por ciudad de origen:", placeholder="Hometown")
unitFilter = sidebar.text_input("Filtrar por Unidad:", placeholder="Unit")
# Search button for applying filters
searchBtn = sidebar.button("Buscar", on_click=filter_df(empIdFilter, hometownFilter, unitFilter))

# Checkbox filter for showing raw data (DF)
showDataCheck = sidebar.checkbox("Mostrar datos", value=True)
sidebar.markdown("---")

# Select box filter for Education Level
educationFilter = sidebar.selectbox("Nivel Educativo:", (["Seleccionar..."] + sorted(df["Education_Level"].unique())))
# Select box filter for City
cityFilter = sidebar.selectbox("Ciudad:", (["Seleccionar..."] + sorted(df["Hometown"].unique())))
# Select box filter for Unit
unitSbFilter = sidebar.selectbox("Unidad:", (["Seleccionar..."] + sorted(df["Unit"].unique())))

df = load_data(BUFF_SIZE, empIdFilter, hometownFilter, unitFilter, educationFilter, cityFilter, unitSbFilter)

# Print total of employees shown
st.write(f"Total de Empleados Mostrados: ***{df.shape[0]}***")

# Create DataFrame widget and run visibility rule
showHideDF(showDataCheck)

#############################################################################################################################################
# Graphs
#############################################################################################################################################

fig, axs = plt.subplots(1, 2, figsize=(11, 8))
# Empleados Agrupados por Edad
sns.set_palette("Set2")
sns.histplot(df["Age"], ax=axs[0])
axs[0].set_title("Histograma de Empleados por Edad")
axs[0].set_ylabel("Total")
axs[0].set_xlabel("Rango Edades")
axs[0].set_xticks(range(int(df["Age"].min()), int(df["Age"].max()) + 1, 5))

# Empleados por Unidad
sns.countplot(x=df["Unit"], ax=axs[1])
axs[1].set_title("Empleados por Unidad")
axs[1].set_ylabel("Total")
axs[1].set_xlabel("")
axs[1].set_xticklabels(axs[1].get_xticklabels(), rotation=90)
plt.tight_layout()
st.pyplot(fig)  


fig2, axs2 = plt.subplots(figsize=(10,4))
# Deserción por Ciudad
sns.lineplot(x=df["Hometown"], y=df["Attrition_rate"], ax=axs2, marker="o")
axs2.set_title("Deserción por Ciudad")
axs2.set_ylabel("Tasa de Deserción")
axs2.set_xlabel("Ciudad")
axs2.set_xticklabels(axs2.get_xticklabels(), rotation=90)
st.pyplot(fig2)


fig3, axs3 = plt.subplots(1, 2, figsize=(10, 6))
# Correlación entre Edad y Tasa de Deserción
sns.scatterplot(x=df["Age"], y=df["Attrition_rate"], ax=axs3[0], hue=df["Time_of_service"])
axs3[0].set_title("Correlación entre Edad y Tasa de Deserción")
axs3[0].set_ylabel("Tasa de Deserción")
axs3[0].set_xlabel("Edad del Empleado")

# Correlación entre Edad y Tasa de Deserción
sns.scatterplot(x=df["Time_of_service"], y=df["Attrition_rate"], ax=axs3[1], hue=df["Age"])
axs3[1].set_title("Correlación entre Tiempo de Servicio y Tasa de Deserción")
axs3[1].set_ylabel("Tasa de Deserción")
axs3[1].set_xlabel("Tiempo de Servicio")
plt.tight_layout()
st.pyplot(fig3)