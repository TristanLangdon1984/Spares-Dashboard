import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Backlog Recovery")

df = pd.read_excel(
    "data/zv308dailyRp21072026.xlsx"
)

backlog = df[
    df["Priority"] == "Late"
]

st.metric(
    "Late Lines",
    len(backlog)
)

st.metric(
    "Late Qty",
    backlog["Qty"].sum()
)

fig = px.histogram(
    backlog,
    x="Owner"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.dataframe(backlog)
