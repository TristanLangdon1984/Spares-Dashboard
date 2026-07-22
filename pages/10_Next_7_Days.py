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

# Product
df["Product"] = df["Material"].apply(
    classify_product
)

today = pd.Timestamp.today().normalize()
week_end = today + pd.Timedelta(days=7)

# Next 7 Days
next_7_days = df[
    (df["Adjusted Target Pack Date"].dt.normalize() > today)
    &
    (df["Adjusted Target Pack Date"].dt.normalize() <= week_end)
].copy()

# Status
next_7_days["Status"] = "❌ Short"

next_7_days.loc[
    next_7_days["StockQty"] >= next_7_days["Qty"],
    "Status"
] = "✅ Can Deliver"

next_7_days["Shortage"] = (
    next_7_days["Qty"]
    - next_7_days["StockQty"]
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

    next_7_days = next_7_days[
        next_7_days["Product"] == product_filter
    ]

if status_filter != "ALL":

    next_7_days = next_7_days[
        next_7_days["Status"] == status_filter
    ]

# KPIs
c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric(
    "Order Lines",
    len(next_7_days)
)

c2.metric(
    "Total Qty",
    int(next_7_days["Qty"].sum())
)

c3.metric(
    "Materials",
    next_7_days["Material"].nunique()
)

c4.metric(
    "Shortage Qty",
    int(
        next_7_days["Shortage"]
        .clip(lower=0)
        .sum()
    )
)

c5.metric(
    "Can Deliver",
    len(
        next_7_days[
            next_7_days["Status"] == "✅ Can Deliver"
        ]
    )
)

c6.metric(
    "Short",
    len(
        next_7_days[
            next_7_days["Status"] == "❌ Short"
        ]
    )
)

# Display
display_df = next_7_days[
    [
        "Doc. Date",
        "Adjusted Target Pack Date",
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
].copy()

display_df.columns = [
    "Doc Date",
    "Pack Date",
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

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    height=900
)
