import streamlit as st
import pandas as pd

from utils.loader import load_backlog

st.title("Next 7 Days")

df = load_backlog()

df["PD Eff.Dte"] = pd.to_datetime(
    df["PD Eff.Dte"],
    dayfirst=True,
    errors="coerce"
)

today = pd.Timestamp.today().normalize()

week_end = today + pd.Timedelta(days=7)

future = df[
    (df["PD Eff.Dte"] > today)
    &
    (df["PD Eff.Dte"] <= week_end)
]

st.metric(
    "Future Lines",
    len(future)
)

st.metric(
    "Qty Due",
    future["Bklg.Qty"].sum()
)

st.dataframe(future)
