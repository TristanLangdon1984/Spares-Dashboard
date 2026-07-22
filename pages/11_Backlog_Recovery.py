import streamlit as st
import pandas as pd

from utils.loader import load_backlog
from config.excluded_parts import EXCLUDED_PARTS
from config.c4c_parts import C4C_PARTS

st.set_page_config(
    page_title="Backlog Recovery",
    layout="wide"
)

st.title("Backlog Recovery")


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

    if material.startswith("S21.") or material.startswith("21."):
        return "BOND"

    if material.startswith("S49.") or material.startswith("49."):
        return "BOND"

    if material.startswith("S26.") or material.startswith("26."):
        return "PELORIS"

    if material.startswith("S45.") or material.startswith("45."):
        return "PELORIS"

    if material.startswith("S33.") or material.startswith("33."):
        return "TBE"

    return "OTHER"


# Load Data
df = load_backlog()

# Remove Excluded Parts
df = df[
    ~df["Material"]
    .astype(str)
    .str.strip()
    .isin(EXCLUDED_PARTS)
]

# Remove C4C Parts
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

df["Adjusted Target Pack Date"] = df["Doc. Date"].apply(
    lambda x: add_business_days(x, 3)
)

# Qty
df["Qty"] = pd.to_numeric(
    df["Bklg.Qty"]
    .astype(str)
    .str.replace(",", ".", regex=False),
    errors="coerce"
).fillna(0)

# Stock
df["StockQty"] = pd.to_numeric(
    df["Stock"]
    .astype(str)
    .str.replace(",", ".", regex=False),
    errors="coerce"
).fillna(0)

# Product Family
df["Product"] = df["Material"].apply(
    classify_product
)

today = pd.Timestamp.today().normalize()

# Backlog
backlog = df[
    df["Adjusted Target Pack Date"].dt.normalize()
    < today
].copy()

# Status
backlog["Status"] = "❌ Short"

backlog.loc[
    backlog["StockQty"] >= backlog["Qty"],
    "Status"
] = "✅ Can Deliver"

backlog["Shortage"] = (
    backlog["Qty"]
    - backlog["StockQty"]
)

# Filters
filter_col1, filter_col2 = st.columns(2)

with filter_col1:

    product_filter = st.radio(
        "Product Family",
        [
            "ALL",
            "BOND",
            "PRIME",
            "PELORIS",
            "TBE",
            "OTHER"
        ],
        horizontal=True
    )

with filter_col2:

    status_filter = st.radio(
        "Delivery Status",
        [
            "ALL",
            "✅ Can Deliver",
            "❌ Short"
        ],
        horizontal=True
    )

if product_filter != "ALL":

    backlog = backlog[
        backlog["Product"] == product_filter
    ]

if status_filter != "ALL":

    backlog = backlog[
        backlog["Status"] == status_filter
    ]

# KPI Cards
c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric(
    "Backlog Lines",
    len(backlog)
)

c2.metric(
    "Backlog Qty",
    int(backlog["Qty"].sum())
)

c3.metric(
    "Materials",
    backlog["Material"].nunique()
)

c4.metric(
    "Shortage Qty",
    int(
        backlog["Shortage"]
        .clip(lower=0)
        .sum()
    )
)

c5.metric(
    "Can Deliver",
    len(
        backlog[
            backlog["Status"] == "✅ Can Deliver"
        ]
    )
)

c6.metric(
    "Short",
    len(
        backlog[
            backlog["Status"] == "❌ Short"
        ]
    )
)

# Display Table
display_df = backlog[
    [
        "Doc. Date",
        "Adjusted Target Pack Date",
        "PD Eff.Dte",
        "Document",
        "Material",
        "Material Description",
        "Qty",
        "StockQty",
