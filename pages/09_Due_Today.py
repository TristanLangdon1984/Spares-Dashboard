import streamlit as st
import pandas as pd

from utils.loader import load_backlog

st.title("Due Today")

df = load_backlog()

date_col = next(
    col for col in df.columns
    if "PD Eff.Dte" in col
)

qty_col = next(
    col for col in df.columns
    if "Bklg.Qty" in col
)

value_col = next(
    col for col in df.columns
    if "Backlog Va" in col
)

df[date_col] = pd.to_datetime(
    df[date_col],
    dayfirst=True,
    errors="coerce"
)

df[qty_col] = pd.to_numeric(
    df[qty_col].astype(str)
    .str.replace(",", ""),
    errors="coerce"
)

df[value_col] = pd.to_numeric(
    df[value_col].astype(str)
    .str.replace(",", ""),
    errors="coerce"
)

today = pd.Timestamp.today().normalize()

due_today = df[
    df[date_col] <= today
]

c1, c2, c3 = st.columns(3)

c1.metric(
    "Lines Due",
    len(due_today)
)

c2.metric(
    "Backlog Qty",
    int(due_today[qty_col].sum())
)

c3.metric(
    "Backlog Value",
    f"${due_today[value_col].sum():,.0f}"
)

st.dataframe(due_today)
