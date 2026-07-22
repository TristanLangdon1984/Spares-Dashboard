import streamlit as st

from utils.loader import load_backlog

st.title("Column Check")

df = load_backlog()

st.write(df.columns.tolist())

st.write(df.shape)

st.dataframe(df.head())
