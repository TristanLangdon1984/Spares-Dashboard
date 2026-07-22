import streamlit as st
import pandas as pd
import plotly.express as px

from utils.value_stream import classify_product

st.title("Value Stream Dashboard")

df = pd.read_excel(
    "data/ZVREP386.xlsx"
)

df["Value Stream"] = df[
    "Material Description"
].apply(classify_product)

summary = (
    df.groupby("Value Stream")
      .agg({
          "Backlog Value":"sum",
          "Bklg.Qty":"sum"
      })
      .reset_index()
)

fig = px.bar(
    summary,
    x="Value Stream",
    y="Backlog Value",
    color="Value Stream"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.dataframe(summary)
