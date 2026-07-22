import streamlit as st
import plotly.express as px

from utils.loader import load_backlog
from utils.value_stream import classify_value_stream

st.title("Value Stream Dashboard")

df = load_backlog()

df["Value Stream"] = df[
    "Material Description"
].apply(
    classify_value_stream
)

summary = (
    df.groupby("Value Stream")
    .agg({
        "Backlog Va":"sum",
        "Bklg.Qty":"sum"
    })
    .reset_index()
)

fig = px.bar(
    summary,
    x="Value Stream",
    y="Backlog Va",
    color="Value Stream"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.dataframe(summary)
