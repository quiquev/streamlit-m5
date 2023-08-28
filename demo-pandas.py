import pandas as pd
import streamlit as st

names_link = "dataset.csv"

# read CSV file
names_df = pd.read_csv(names_link)

# create title
st.title("Streamlit + Pandas!!!")
# print dataframe
st.dataframe(names_df, width=800)
