import streamlit as st
from utils.loader import load_metrics

st.title("Executive Overview")

metrics = load_metrics()

latest = metrics.iloc[-1]

col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "Late Lines",
    latest.iloc[1]
)

col2.metric(
    "Open Lines",
    latest.iloc[3]
)

col3.metric(
    "Due Next 4 Days",
    latest.iloc[2]
)

col4.metric(
    "Date",
    str(latest.iloc[0])[:10]
)

st.dataframe(metrics.tail())
