import streamlit as st
import plotly.express as px

from utils.loader import load_metrics

st.title("Backlog Control Tower")

df = load_metrics()

fig = px.line(
    df,
    x="Date",
    y="Open Lines Remaining",
    markers=True,
    title="Open Lines Remaining"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

fig2 = px.line(
    df,
    x="Date",
    y="Late Lines",
    markers=True,
    title="Late Lines"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)
