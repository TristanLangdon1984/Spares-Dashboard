import streamlit as st
import pandas as pd
import plotly.express as px

from utils.loader import load_backlog

st.title("Value Stream Dashboard")

df = load_backlog()

material_col = next(
    col for col in df.columns
    if "Material Description" in col
)

qty_col = next(
    col for col in df.columns
    if "Bklg.Qty" in col
)

value_col = next(
    col for col in df.columns
    if "Backlog Va" in col
)


def classify_value_stream(desc):

    desc = str(desc).upper()

    if "PELORIS" in desc:
        return "PELORIS"

    if "CER" in desc:
        return "CER"

    if "ARC" in desc:
        return "ARC"

    if (
        "BOND" in desc
        or "PRIME" in desc
        or "RX" in desc
        or "BOND-III" in desc
        or "BOND III" in desc
        or "BOND-MAX" in desc
    ):
        return "BOND"

    return "OTHER"


df["Value Stream"] = df[material_col].apply(
    classify_value_stream
)

df[qty_col] = pd.to_numeric(
    df[qty_col].astype(str)
    .str.replace(",", ""),
    errors="coerce"
)

df[value_col] = pd.to_numeric(
    df[value_col].astype(str)
    .str.replace(",", "")
    .str.replace(" ", ""),
    errors="coerce"
)

summary = (
    df.groupby("Value Stream")
    .agg({
        qty_col: "sum",
        value_col: "sum"
    })
    .reset_index()
)

st.dataframe(summary)

fig = px.bar(
    summary,
    x="Value Stream",
    y=value_col,
    color="Value Stream",
    title="Backlog Value by Value Stream"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
