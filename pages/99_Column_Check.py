import streamlit as st
from utils.loader import load_metrics

df = load_metrics()

st.write(df.columns.tolist())
