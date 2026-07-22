import streamlit as st
import pandas as pd

from utils.loader import load_backlog

st.title("Next 7 Days")

df = load_backlog()

date_col = next(
    col for col in df.columns
    if "PD Eff.Dte" in col
)

df[date_col] = pd.to_datetime(
    df[date_col],
    dayfirst=True,
    errors="coerce"
)

today = pd.Timestamp.today().normalize()
week_end = today + pd.Timedelta(days=7)

future = df[
    (df[date_col] > today)
    &
    (df[date_col] <= week_end)
]

st.metric(
    "Order Lines",
    len(future)
)

st.dataframe(future)
