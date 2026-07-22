import streamlit as st

from utils.loader import load_backlog

st.title("Value Stream Dashboard")

df = load_backlog()

st.write(df.shape)

st.write(df.columns.tolist())

st.dataframe(df.head())
