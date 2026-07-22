import streamlit as st
import plotly.express as px

from utils.loader import load_metrics

st.title("Operations Dashboard")

df = load_metrics()

fig = px.bar(
    df,
    x="Date",
    y=["Raised","Produced"],
    barmode="group",
    title="Orders Raised vs Produced"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

fig2 = px.line(
    df,
    x="Date",
    y="Overproduction Rate",
    markers=True,
    title="Overproduction Rate"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)
