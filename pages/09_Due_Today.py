import streamlit as st
import pandas as pd

st.title("Due Today")

df = pd.read_excel(
    "data/zv308dailyRp21072026.xlsx"
)

today = df[
    df["Priority"] == "Today"
]

st.metric(
    "Order Lines",
    len(today)
)

st.metric(
    "Total Qty",
    today["Qty"].sum()
)

st.dataframe(today)
