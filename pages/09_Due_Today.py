import streamlit as st
import pandas as pd

from utils.loader import load_backlog

st.title("Due Today")

df = load_backlog()

# Convert date column
df["PD Eff.Dte"] = pd.to_datetime(
    df["PD Eff.Dte"],
    dayfirst=True,
    errors="coerce"
)

# Convert quantity column
df["Bklg.Qty"] = pd.to_numeric(
    df["Bklg.Qty"],
    errors="coerce"
)

# Convert stock column
df["Stock"] = pd.to_numeric(
    df["Stock"],
    errors="coerce"
)

today = pd.Timestamp.today().normalize()

# Due today or overdue
due_today = df[df["PD Eff.Dte"] <= today].copy()

# Shortage calculation
due_today["Shortage"] = (
    due_today["Bklg.Qty"].fillna(0)
    - due_today["Stock"].fillna(0)
)

# KPI row
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Order Lines Due",
    len(due_today)
)

col2.metric(
    "Backlog Qty",
    f"{due_today['Bklg.Qty'].sum():,.0f}"
)

col3.metric(
    "Materials",
    due_today["Material"].nunique()
)

col4.metric(
    "Shortage Qty",
    f"{due_today['Shortage'].clip(lower=0).sum():,.0f}"
)

# Display columns
display_df = due_today[
    [
        "Doc. Date",
        "RSD",
        "PD Eff.Dte",
        "Document",
        "Material",
        "Material Description",
        "Bklg.Qty",
        "Stock",
        "ShipToCtry",
        "Plnt",
        "Express De"
    ]
].sort_values(
    by="PD Eff.Dte"
)

st.subheader("Due Today / Overdue Orders")

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)
