import streamlit as st
from utils.loader import load_backlog

df = load_backlog()

st.write(df.shape)
st.write(df.columns.tolist())
