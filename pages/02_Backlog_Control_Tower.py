import streamlit as st
import plotly.express as px

from utils.loader import load_metrics

st.title("Backlog Control Tower")

df = load_metrics()

fig = px.line(
    df,
    x=df.columns[0],
    y=df.columns[-4],
    markers=True,
    title="Backlog Trend"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.dataframe(df.tail(20))
