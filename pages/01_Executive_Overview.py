import streamlit as st
import plotly.express as px

from utils.loader import load_metrics

st.title("Executive Overview")

df = load_metrics()

latest = df.iloc[-1]

col1,col2,col3,col4,col5,col6 = st.columns(6)

col1.metric(
    "Late Lines",
    int(latest["Late Lines"])
)

col2.metric(
    "Due Next 4 Days",
    int(latest["Ok Lines Due Next 4 Days"])
)

col3.metric(
    "Open Lines",
    int(latest["Open Lines Remaining"])
)

col4.metric(
    "Backlog",
    int(latest["Backlog"])
)

col5.metric(
    "Produced",
    int(latest["Produced"])
)

col6.metric(
    "Raised",
    int(latest["Raised"])
)

st.divider()

fig = px.line(
    df,
    x="Date",
    y="Backlog",
    markers=True,
    title="Backlog Trend"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
