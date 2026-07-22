import streamlit as st
import pandas as pd

from utils.loader import load_backlog
from config.excluded_parts import EXCLUDED_PARTS
from config.c4c_parts import C4C_PARTS

st.set_page_config(
    page_title="Next 7 Days",
    layout="wide"
)

st.title("Next 7 Days")


def add_business_days(start_date, business_days):

    if pd.isna(start_date):
        return pd.NaT

    current_date = start_date
    days_added = 0

    while days_added < business_days:

        current_date = current_date + pd.Timedelta(days=1)

        if current_date.weekday() < 5:
            days_added += 1

    return current_date


def classify_product(material):

    material = str(material).upper().strip()

    if material.startswith("S091.") or material.startswith("91."):
        return "PRIME"

    if (
        material.startswith("S21.")
        or material.startswith("21.")
        or material.startswith("S49.")
        or material.startswith("49.")
    ):
        return "BOND"

    if (
        material.startswith("S26.")
        or material.startswith("26.")
        or material.startswith("S45.")
        or material.startswith("45.")
    ):
        return "PELORIS"

    if (
        material.startswith("S33.")
        or material.startswith("33.")
    ):
        return "TBE"

    return "OTHER"


# Load Data
df = load_backlog()

# Remove excluded parts
df = df[
    ~df["Material"].astype(str).str.strip().isin(EXCLUDED_PARTS)
]

# Capture C4C
c4c_df = df[
    df["Material"].astype(str).str.strip().isin(C4C_PARTS)
].copy()

# Remove C4C from operational queue
df = df[
    ~df["Material"].astype(str).str.strip().isin(C4C_PARTS)
]

# Dates
df["Doc. Date"] = pd.to_datetime(
    df["Doc. Date"],
    dayfirst=True,
    errors="coerce"
)

df["Adjusted Target Pack Date"] = df[
    "Doc. Date"
].apply(
    lambda x: add_business_days(x, 3)
)

# Quantity
df["Qty"] = (
    df["Bklg.Qty"]
    .astype(str)
    .str.replace(",", ".", regex=False)
)

df["Qty"] = pd.to_numeric(
    df["Qty"],
    errors="coerce"
).fillna(0).astype(int)

# Stock
df["StockQty"] = (
    df["Stock"]
    .astype(str)
    .str.replace(",", ".", regex=False)
)

df["StockQty"] = pd.to_numeric(
    df["StockQty"],
    errors="coerce"
).fillna(0).astype(int)

# Product classification
df["Product"] = df["Material"].apply(
    classify_product
)

today = pd.Timestamp.today().normalize()
week_end = today + pd.Timedelta(days=7)

# Next 7 Days
next_7_days = df[
    (
        df["Adjusted Target Pack Date"].dt.normalize()
        > today
    )
    &
    (
        df["Adjusted Target Pack Date"].dt.normalize()
        <= week_end
    )
].copy()

# Status
next_7_days["Status"] = "❌ Short"

mask = (
    next_7_days["StockQty"]
    >= next_7_days["Qty"]
)

next_7_days.loc[
    mask,
    "Status"
] = "✅ Can Deliver"

next_7_days["Shortage"] = (
    next_7_days["Qty"]
    - next_7_days["StockQty"]
)

# Product filter
product_filter = st.radio(
    "Product Family",
    ["ALL", "BOND", "PRIME", "PELORIS", "TBE", "OTHER"],
    horizontal=True
)

if product_filter != "ALL":

    next_7_days = next_7_days[
        next_7_days["Product"] == product_filter
    ]

# KPIs
c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Order Lines",
    len(next_7_days)
)

c2.metric(
    "Total Qty",
    f"{next_7_days['Qty'].sum():,.0f}"
)

