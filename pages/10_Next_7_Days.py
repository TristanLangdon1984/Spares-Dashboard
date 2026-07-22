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

        current_date += pd.Timedelta(days=1)

        if current_date.weekday() < 5:
            days_added += 1

    return current_date


df = load_backlog()

# Excluded materials
df = df[
    ~df["Material"]
    .astype(str)
    .str.strip()
    .isin(EXCLUDED_PARTS)
]

# C4C materials
c4c_df = df[
    df["Material"]
    .astype(str)
    .str.strip()
    .isin(C4C_PARTS)
].copy()

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

df["Adjusted Target Pack Date"] = df[
    "Doc. Date"
].apply(
    lambda x: add_business_days(x, 3)
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
week_end = today + pd.Timedelta(days=7)

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

next_7_days["Status"] = "❌ Short"

next_7_days.loc[
    next_7_days["StockQty"] >= next_7_days["Qty"],
    "Status"
] = "✅ Can Deliver"

col1, col2, col3 = st.columns(3)

col1.metric(
    "Order Lines",
    len(next_7_days)
)

col2.metric(
    "Qty",
    f"{next_7_days['Qty'].sum():,.0f}"
)

col3.metric(
    "Materials",
    next_7_days["Material"].nunique()
)

display_df = next_7_days[
    [
        "Adjusted Target Pack Date",
        "Material",
        "Material Description",
        "Qty",
        "StockQty",
        "Status"
    ]
]

display_df.columns = [
    "Pack Date",
    "Material",
    "Description",
    "Qty",
    "Stock",
    "Status"
]

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

st.subheader("C4C Parts")

st.dataframe(
    c4c_df[
        [
            "Material",
            "Material Description"
        ]
    ],
