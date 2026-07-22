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
    df["Bklg.Qty"],
    errors="coerce"
)

today = pd.Timestamp.today().normalize()

due_today = df[
    df["PD Eff.Dte"] <= today
]

c1, c2 = st.columns(2)

c1.metric(
    "Order Lines Due",
    len(due_today)
)

c2.metric(
    "Backlog Qty",
    int(due_today["Bklg.Qty"].fillna(0).sum())
)

st.dataframe(
    due_today[
        [
            "Document",
            "Material",
            "Material Description",
            "Bklg.Qty",
            "Stock",
            "ShipToCtry",
            "Plnt",
            "PD Eff.Dte",
            "Express De"
        ]
    ],
    use_container_width=True
)
