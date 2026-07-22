import streamlit as st
import pandas as pd

from utils.loader import load_backlog
from config.excluded_parts import EXCLUDED_PARTS

st.set_page_config(
    page_title="Due Today",
    layout="wide"
)

st.title("Due Today")

# Load backlog
df = load_backlog()

# Remove excluded materials
df = df[
    ~df["Material"]
    .astype(str)
    .str.strip()
    .isin(EXCLUDED_PARTS)
]

# Convert dates
df["PD Eff.Dte"] = pd.to_datetime(
    df["PD Eff.Dte"],
    dayfirst=True,
    errors="coerce"
)

# Convert quantity
df["Bklg.Qty"] = pd.to_numeric(
    df["Bklg.Qty"],
    errors="coerce"
)

# Convert stock
df["Stock"] = pd.to_numeric(
    df["Stock"],
    errors="coerce"
)

today = pd.Timestamp.today().normalize()

# Only show records from the last 3 months
three_months_ago = today - pd.DateOffset(months=3)

df = df[
    df["PD Eff.Dte"] >= three_months_ago
]

# Due today and overdue
due_today = df[
    df["PD Eff.Dte"] <= today
].copy()

# Shortage calculation
due_today["Shortage"] = (
    due_today["Bklg.Qty"].fillna(0)
    - due_today["Stock"].fillna(0)
)

# KPI Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Order Lines Due",
        len(due_today)
    )

with col2:
    st.metric(
        "Backlog Qty",
        f"{due_today['Bklg.Qty'].sum():,.0f}"
    )

with col3:
    st.metric(
        "Materials",
        due_today["Material"].nunique()
    )

with col4:
    st.metric(
        "Shortage Qty",
        f"{due_today['Shortage'].clip(lower=0).sum():,.0f}"
    )

# Table
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
    by="PD Eff.Dte",
    ascending=True
)

display_df.columns = [
    "Doc Date",
    "RSD",
    "Due Date",
    "Order",
    "Material",
    "Description",
    "Qty",
    "Stock",
    "Country",
    "Plant",
    "Express"
]

st.subheader("Due Today / Overdue Orders (Last 3 Months)")

st.table(display_df)

with st.expander("Excluded Materials"):
    st.table(
        pd.DataFrame(
            {"Material": EXCLUDED_PARTS}
        )
    )
