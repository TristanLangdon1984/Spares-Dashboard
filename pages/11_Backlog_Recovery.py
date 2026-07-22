import streamlit as st
import pandas as pd
import plotly.express as px

from utils.loader import load_backlog

st.title("Backlog Recovery")

df = load_backlog()

pastdue_col = next(
    col for col in df.columns
    if "PastDue" in col
)

value_col = next(
    col for col in df.columns
    if "Backlog Va" in col
)

material_col = next(
    col for col in df.columns
    if "Material Description" in col
)

df[value_col] = pd.to_numeric(
    df[value_col].astype(str)
    .str.replace(",", ""),
    errors="coerce"
)

backlog = df[
    df[pastdue_col]
    .astype(str)
    .str.contains("X", na=False)
]

st.metric(
    "Past Due Lines",
    len(backlog)
)

top = (
    backlog.groupby(material_col)[value_col]
    .sum()
    .sort_values(ascending=False)
    .head(15)
)

fig = px.bar(
    top,
    title="Top Backlog Materials"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.dataframe(backlog)
