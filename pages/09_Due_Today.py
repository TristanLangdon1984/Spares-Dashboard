import streamlit as st
import pandas as pd

from utils.loader import load_backlog

st.set_page_config(
    page_title="Due Today",
    layout="wide"
)

st.title("Due Today")

df = load_backlog()

# Clean data
df["PD Eff.Dte"] = pd.to_datetime(
    df["PD Eff.Dte"],
    dayfirst=True,
    errors="coerce"
)

df["Bklg.Qty"] = pd.to_numeric(
    df["Bklg.Qty"],
    errors="coerce"
)

df["Stock"] = pd.to_numeric(
    df["Stock"],
    errors="coerce"
)

today = pd.Timestamp.today().normalize()

# Due today and overdue
due_today = df[
    df["PD Eff.Dte"] <= today
].copy()

# KPIs
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Order Lines Due",
        len(due_today)
    )

with col2:
    st.metric(
        "Backlog Qty",
        f"{due_today['Bklg.Qty'].fillna(0).sum():,.0f}"
    )

with col3:
    st.metric(
        "Materials",
        due_today["Material"].nunique()
    )

