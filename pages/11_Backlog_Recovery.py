import streamlit as st
import plotly.express as px
import pandas as pd

from utils.loader import load_backlog

st.title("Backlog Recovery")

df = load_backlog()

backlog = df[
    df["PastDue"].astype(str).str.contains(
        "X",
        na=False
    )
]

st.metric(
    "Late Lines",
    len(backlog)
)

top = (
    backlog.groupby(
        "Material Description"
    )["Backlog Va"]
    .sum()
    .sort_values(
        ascending=False
    )
    .head(20)
)

fig = px.bar(
    top,
    title="Top Backlog Materials"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
