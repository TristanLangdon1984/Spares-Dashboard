import streamlit as st
import pandas as pd

from utils.loader import load_backlog

st.set_page_config(
    page_title="Next 7 Days",
    layout="wide"
)

st.title("Next 7 Days")

df = load_backlog()

# Dates
df["Doc. Date"] = pd.to_datetime(
    df["Doc. Date"],
    dayfirst=True,
    errors="coerce"
)

today = pd.Timestamp.today().normalize()
week_end = today + pd.Timedelta(days=7)

# Show next 7 days using PD Eff.Dte for now
df["PD Eff.Dte"] = pd.to_datetime(
    df["PD Eff.Dte"],
    dayfirst=True,
    errors="coerce"
)

next_7_days = df[
    (
        df["PD Eff.Dte"].dt.normalize() > today
    )
    &
    (
        df["PD Eff.Dte"].dt.normalize() <= week_end
    )
].copy()

# Qty
next_7_days["Qty"] = (
    next_7_days["Bklg.Qty"]
    .astype(str)
    .str.replace(",", ".", regex=False)
)

next_7_days["Qty"] = pd.to_numeric(
    next_7_days["Qty"],
    errors="coerce"
).fillna(0).astype(int)

# KPIs
col1, col2 = st.columns(2)

col1.metric(
    "Order Lines",
    len(next_7_days)
)

col2.metric(
    "Total Qty",
    f"{next_7_days['Qty'].sum():,.0f}"
)

# TABLE
st.subheader("Orders Due Next 7 Days")

display_df = next_7_days[
    [
        "Doc. Date",
        "PD Eff.Dte",
        "Document",
        "Material",
        "Material Description",
        "Qty",
        "Stock",
        "ShipToCtry",
        "Plnt"
    ]
].copy()

display_df.columns = [
    "Doc Date",
    "Due Date",
    "Order",
    "Material",
