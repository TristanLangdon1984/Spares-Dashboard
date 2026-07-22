import streamlit as st
import pandas as pd

from utils.loader import load_backlog

st.title("Quantity Debug")

df = load_backlog()

st.write("Original Values")
st.dataframe(df[["Bklg.Qty"]].head(20))

df["Bklg.Qty_Test"] = (
    df["Bklg.Qty"]
    .astype(str)
    .str.replace(",", ".", regex=False)
)

st.write("After Replace")
st.dataframe(df[["Bklg.Qty", "Bklg.Qty_Test"]].head(20))

df["Bklg.Qty_Num"] = pd.to_numeric(
    df["Bklg.Qty_Test"],
    errors="coerce"
)

st.write("After Numeric Conversion")
st.dataframe(
    df[
        [
            "Bklg.Qty",
            "Bklg.Qty_Test",
            "Bklg.Qty_Num"
        ]
    ].head(20)
)

st.write(df["Bklg.Qty_Num"].dtype)
