import streamlit as st
import pandas as pd

st.title("Next 7 Days")

df = pd.read_excel(
    "data/zv308dailyRp21072026.xlsx"
)

future = df[
    df["Priority"] == "Next Due"
]

st.metric(
    "Future Lines",
    len(future)
)

st.metric(
    "Future Qty",
    future["Qty"].sum()
)

st.dataframe(future)
