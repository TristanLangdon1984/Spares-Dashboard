import streamlit as st
import pandas as pd
import plotly.express as px

from utils.loader import load_backlog

st.title("Value Stream Dashboard")

df = load_backlog()


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
    ):
        return "BOND"

    return "OTHER"


df["Value Stream"] = df["Material Description"].apply(
    classify_value_stream
)

df["Backlog Va"] = pd.to_numeric(
    df["Backlog Va"]
        .astype(str)
        .str.replace(",", ""),
    errors="coerce"
)

df["Bklg.Qty"] = pd.to_numeric(
    df["Bklg.Qty"]
        .astype(str)
        .str.replace(",", ""),
    errors="coerce"
)

summary = (
    df.groupby("Value Stream")
      .agg({
          "Backlog Va": "sum",
          "Bklg.Qty": "sum"
      })
      .reset_index()
)

c1, c2, c3 = st.columns(3)

c1.metric(
    "Total Backlog Value",
    f"${summary['Backlog Va'].sum():,.0f}"
)

c2.metric(
    "Total Backlog Qty",
    f"{summary['Bklg.Qty'].sum():,.0f}"
)

c3.metric(
    "Value Streams",
    summary["Value Stream"].nunique()
)

fig = px.bar(
    summary,
    x="Value Stream",
    y="Backlog Va",
    color="Value Stream",
    title="Backlog Value by Value Stream"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.dataframe(summary)
