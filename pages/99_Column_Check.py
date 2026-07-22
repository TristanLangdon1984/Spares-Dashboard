import streamlit as st

from utils.loader import load_backlog

st.title("Column Check")

df = load_backlog()

st.write("Rows, Columns")
st.write(df.shape)

st.write("Columns")
st.write(df.columns.tolist())

st.dataframe(df.head(20))
