import streamlit as st

myName = st.text_input("Nombre:")

if (myName):
    st.write(f"Tu nombre es: {myName}")