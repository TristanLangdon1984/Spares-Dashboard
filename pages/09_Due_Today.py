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

today = pd.Timestamp.today().normalize()

due_today = df[
    df["PD Eff.Dte"] <= today
]

c1, c2, c3 = st.columns(3)

c1.metric(
    "Lines Due",
    len(due_today)
)

c2.metric(
    "Backlog Qty",
    due_today["Bklg.Qty"].sum()
)

c3.metric(
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
