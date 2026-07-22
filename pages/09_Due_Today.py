import streamlit as st
import pandas as pd

from utils.loader import load_backlog
from config.c4c_parts import C4C_PARTS

st.set_page_config(
    page_title="Due Today",
    layout="wide"
)

st.title("Due Today")


def add_business_days(start_date, business_days):

    if pd.isna(start_date):
        return pd.NaT

    date = start_date

    days_added = 0

    while days_added < business_days:

        date = date + pd.Timedelta(days=1)

        if date.weekday() < 5:
            days_added += 1

    return date


# Load backlog
df = load_backlog()

# Exclude normal exclusions
df = df[
    ~df["Material"]
    .astype(str)
    .str.strip()
    .isin(EXCLUDED_PARTS)
]

# Create C4C dataset
c4c_df = df[
    df["Material"]
    .astype(str)
    .str.strip()
    .isin(C4C_PARTS)
].copy()

# Remove C4C parts from Due Today list
df = df[
    ~df["Material"]
    .astype(str)
    .str.strip()
    .isin(C4C_PARTS)
]


# Dates
df["Doc. Date"] = pd.to_datetime(
    df["Doc. Date"],
    dayfirst=True,
    errors="coerce"
)

df["PD Eff.Dte"] = pd.to_datetime(
    df["PD Eff.Dte"],
    dayfirst=True,
    errors="coerce"
)

# Create Adjusted Target Pack Date
df["Adjusted Target Pack Date"] = df[
    "Doc. Date"
].apply(
    lambda x: add_business_days(x, 3)
)

# Qty conversion
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

# Stock conversion
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

# Due Today based on Adjusted Target Pack Date
due_today = df[
    df["Adjusted Target Pack Date"].dt.normalize()
    == today
].copy()

# Shortage calculation
due_today["Shortage"] = (
    due_today["Qty"]
    - due_today["StockQty"]
)

# Status
due_today["Status"] = due_today.apply(
    lambda x:
    "✅ Can Deliver"
    if x["StockQty"] >= x["Qty"]
    else "❌ Short",
    axis=1
)

# KPIs
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Orders Due Today",
    len(due_today)
)

col2.metric(
    "Total Qty",
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
        "Adjusted Target Pack Date",
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
]

display_df = display_df.sort_values(
    by=[
        "Adjusted Target Pack Date",
        "Material"
    ]
)

display_df.columns = [
    "Doc Date",
    "Adjusted Target Pack Date",
    "Original Due Date",
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

def highlight_row(row):

    if "Can Deliver" in row["Status"]:
        return [
            "background-color:#d4edda"
        ] * len(row)

    return [
        "background-color:#f8d7da"
    ] * len(row)


st.subheader("Orders Due Today")

st.dataframe(
    display_df.style.apply(
        highlight_row,
        axis=1
    ),
    use_container_width=True,
    hide_index=True,
    height=900
)
