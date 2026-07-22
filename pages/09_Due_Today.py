import streamlit as st
import pandas as pd

from utils.loader import load_backlog

st.title("Due Today Debug")

df = load_backlog()

st.write("Columns")
st.write(df.columns.tolist())

st.write("Bklg.Qty Raw Values")
st.write(df["Bklg.Qty"].head(20))

st.write("Bklg.Qty Data Type")
st.write(df["Bklg.Qty"].dtype)

st.write("Unique Sample Values")
st.write(df["Bklg.Qty"].dropna().head(50).tolist())

st.write(
    df[
        ["Material", "Bklg.Qty"]
    ].head(20)
)
