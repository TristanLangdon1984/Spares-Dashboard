import streamlit as st

with open(
    "data/ZVREP386 - 3013BACKLOG1.XLS",
    "rb"
) as f:

    raw = f.read(200)

st.write(raw)
