import streamlit as st
import pandas as pd

from utils.loader import load_backlog

st.title("Due Today")

df = load_backlog()

df["PD Eff.Dte"] = pd.to_datetime(
    df["PD Eff.Dte"],
    dayfirst=True,
    errors="coerce"
)

df["Bklg.Qty"] = pd.to_numeric(
    df["Bklg.Qty"]
        .astype(str)
        .str.replace(",", ""),
    errors="coerce"
)

df["Backlog Va"] = pd.to_numeric(
    df["Backlog Va"]
        .astype(str)
        .str.replace(",", ""),
    errors="coerce"
)

today = pd.Timestamp.today().normalize()

due_today = df[
    df["PD Eff.Dte"] <= today
]

st.metric(
    "Lines Due",
    len(due_today)
)

st.metric(
    "Backlog Qty",
    int(due_today["Bklg.Qty"].sum())
)

st.metric(
    "Backlog Value",
    f"${due_today['Backlog Va'].sum():,.0f}"
)

st.dataframe(
    due_today[
        [
            "Material",
            "Material Description",
            "Bklg.Qty",
            "Stock",
            "Customer name",
            "PD Eff.Dte"
        ]
    ]
)
