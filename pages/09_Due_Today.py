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

# Exclude materials
df = df[
    ~df["Material"]
    .astype(str)
    .str.strip()
    .isin(EXCLUDED_PARTS)
]

# Dates
df["PD Eff.Dte"] = pd.to_datetime(
    df["PD Eff.Dte"],
    dayfirst=True,
    errors="coerce"
)

# Qty
df["Qty"] = (
    df["Bklg.Qty"]
    .astype(str)
    .str.replace(",", ".", regex=False)
)

df["Qty"] = (
    pd.to_numeric(
        df["Qty"],
        errors="coerce"
    )
    .fillna(0)
    .astype(int)
)

# Stock
df["StockQty"] = (
    df["Stock"]
    .astype(str)
    .str.replace(",", ".", regex=False)
)

df["StockQty"] = (
    pd.to_numeric(
        df["StockQty"],
        errors="coerce"
    )
    .fillna(0)
    .astype(int)
)

today = pd.Timestamp.today().normalize()

# Due Today Only
due_today = df[
    df["PD Eff.Dte"].dt.normalize() == today
].copy()

# Shortage
due_today["Shortage"] = (
    due_today["Qty"]
    - due_today["StockQty"]
)

# Status
due_today["Status"] = due_today.apply(
    lambda x:
    "Can Deliver"
    if x["StockQty"] >= x["Qty"]
    else "Short",
    axis=1
)

# KPI Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Orders Due Today",
        len(due_today)
    )

with col2:
    st.metric(
        "Total Qty",
        f"{due_today['Qty'].sum():,.0f}"
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

# Display table
display_df = due_today[
    [
        "Doc. Date",
        "RSD",
        "PD Eff.Dte",
        "Document",
        "Material",
        "Material Description",
        "Qty",
        "StockQty",
        "Status",
        "ShipToCtry",
        "Plnt",
        "Express De"
    ]
].sort_values(
    by=["Status", "Material"]
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
    "Status",
    "Country",
    "Plant",
    "Express"
]

def colour_status(row):

    if row["Status"] == "Can Deliver":
        return ["background-color:#d4edda"] * len(row)

    return ["background-color:#f8d7da"] * len(row)

st.subheader("Due Today Orders")

st.dataframe(
    display_df.style.apply(
        colour_status,
        axis=1
    ),
    use_container_width=True,
    hide_index=True,
    height=900
)
