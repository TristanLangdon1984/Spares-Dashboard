import streamlit as st
import pandas as pd

from utils.loader import load_backlog
from config.excluded_parts import EXCLUDED_PARTS

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

    if material.startswith("S33.") or material.startswith("33."):
        return "TBE"

    return "OTHER"


df = load_backlog()

# Remove excluded materials
df = df[
    ~df["Material"]
    .astype(str)
    .str.strip()
    .isin(EXCLUDED_PARTS)
]

df["Doc. Date"] = pd.to_datetime(
    df["Doc. Date"],
    dayfirst=True,
    errors="coerce"
)

df["Adjusted Target Pack Date"] = df["Doc. Date"].apply(
    lambda x: add_business_days(x, 3)
)

df["Qty"] = pd.to_numeric(
    df["Bklg.Qty"]
    .astype(str)
    .str.replace(",", ".", regex=False),
    errors="coerce"
).fillna(0)

df["Product"] = df["Material"].apply(
    classify_product
)

today = pd.Timestamp.today().normalize()

week_end = today + pd.Timedelta(days=7)

next_7_days = df[
    (df["Adjusted Target Pack Date"].dt.normalize() > today)
    &
    (df["Adjusted Target Pack Date"].dt.normalize() <= week_end)
].copy()

# Product Filter
product_filter = st.radio(
    "Product Family",
    ["ALL", "BOND", "PRIME", "PELORIS", "TBE", "OTHER"],
    horizontal=True
)

if product_filter != "ALL":

    next_7_days = next_7_days[
        next_7_days["Product"] == product_filter
    ]

st.metric(
    "Order Lines",
    len(next_7_days)
)

st.metric(
    "Total Qty",
    int(next_7_days["Qty"].sum())
)

display_df = next_7_days.copy()

display_df = display_df.rename(
    columns={

