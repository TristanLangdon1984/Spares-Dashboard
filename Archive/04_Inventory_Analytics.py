import streamlit as st
import plotly.express as px

from utils.loader import load_parts

st.title("Inventory Analytics")

df = load_parts()

top = df.nlargest(
    20,
    "Total conspt"
)

fig = px.bar(
    top,
    x="Total conspt",
    y="Material Description",
    orientation="h",
    title="Top Consumed Parts"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.dataframe(top)
