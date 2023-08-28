import streamlit as st

def bienvenida(nombre):
    mensaje = "Bienvenid@: " + nombre
    return mensaje

# read name 
miNombre = st.text_input("Nombre:")

if (miNombre):
    # call 
    st.write(bienvenida(miNombre))