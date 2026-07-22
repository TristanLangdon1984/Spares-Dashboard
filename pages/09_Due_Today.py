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

# Shortage
due_today["Shortage"] = (
    due_today["Qty"]
    - due_today["StockQty"]
)

# Delivery Status
due_today["Status"] = due_today.apply(
    lambda row: "✅ Can Deliver"
    if row["StockQty"] >= row["Qty"]
    else "❌ Short"
    ,
    axis=1
)

# KPIs
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

