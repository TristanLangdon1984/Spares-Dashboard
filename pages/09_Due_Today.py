import streamlit as st
import pandas as pd

from utils.loader import load_backlog
from config.excluded_parts import EXCLUDED_PARTS

st.set_page_config(
    page_title="Due Today",
    layout="wide"
)

st.title("Due Today")

# Load data
df = load_backlog()

# Exclude materials
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
df["Qty"] = (
    df["Bklg.Qty"]
    .astype(str)
    .str.replace(",", ".", regex=False)
    .str.strip()
)

df["Qty"] = (
    pd.to_numeric(
        df["Qty"],
        errors="coerce"
    )
    .fillna(0)
    .astype(int)
)

# Convert stock
df["StockQty"] = (
    df["Stock"]
    .astype(str)
    .str.replace(",", ".", regex=False)
    .str.strip()
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

# Due today only
due_today = df[
    df["PD Eff.Dte"].dt.normalize() == today
].copy()

# Shortages
due_today["Shortage"] = (
    due_today["Qty"]
    - due_today["StockQty"]
)

# KPI row
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Order Lines Due Today",
    len(due_today)
)

col2.metric(
    "Backlog Qty",
    f"{due_today['Qty'].sum():,.0f}"
)

col3.metric(
    "Unique Materials",
    due_today["Material"].nunique()
)

col4.metric(
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
        "ShipToCtry",
        "Plnt",
        "Express De"
    ]
].sort_values(
    by="PD Eff.Dte"
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

st.subheader("Due Today")

st.table(display_df)
