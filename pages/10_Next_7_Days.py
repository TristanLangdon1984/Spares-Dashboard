
import streamlit as st
import pandas as pd

from utils.loader import load_backlog

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

# Convert dates
df["Doc. Date"] = pd.to_datetime(
    df["Doc. Date"],
    dayfirst=True,
    errors="coerce"
)

# Calculate Adjusted Target Pack Date
df["Adjusted Target Pack Date"] = (
    df["Doc. Date"]
    .apply(lambda x: add_business_days(x, 3))
)

# Convert Qty
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

today = pd.Timestamp.today().normalize()

week_end = today + pd.Timedelta(days=7)

# Next 7 days based on Adjusted Target Pack Date
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

# KPI
col1, col2 = st.columns(2)

col1.metric(
    "Order Lines",
    len(next_7_days)
)

col2.metric(
    "Total Qty",
    f"{next_7_days['Qty'].sum():,.0f}"
)

# Table
display_df = next_7_days[
    [
        "Doc. Date",
        "Adjusted Target Pack Date",
        "Material",
        "Material Description",
        "Qty",
        "Stock"
    ]
].copy()

display_df.columns = [
    "Doc Date",
    "Pack Date",
    "Material",
    "Description",
    "Qty",
    "Stock"
]

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    height=900
)
