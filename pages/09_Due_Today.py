import streamlit as st
import pandas as pd

from utils.loader import load_backlog

st.title("Due Today")

# Load data
df = load_backlog()

# Convert dates
df["PD Eff.Dte"] = pd.to_datetime(
    df["PD Eff.Dte"],
    dayfirst=True,
    errors="coerce"
)

# Convert quantities
df["Bklg.Qty"] = pd.to_numeric(
    df["Bklg.Qty"],
    errors="coerce"
)

# Convert stock
df["Stock"] = pd.to_numeric(
    df["Stock"],
    errors="coerce"
)

today = pd.Timestamp.today().normalize()

# Due today and overdue orders
due_today = df[
    df["PD Eff.Dte"] <= today
].copy()

# Shortage calculation
due_today["Shortage"] = (
    due_today["Bklg.Qty"].fillna(0)
    - due_today["Stock"].fillna(0)
)

# KPI Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Order Lines Due",
        len(due_today)
    )

with col2:
    st.metric(
        "Backlog Qty",
        f"{due_today['Bklg.Qty'].sum():,.0f}"
    )

with col3:
    st.metric(
        "Materials",
        due_today["Material"].nunique()
    )

with col4:
    st.metric(
        "Shortage Qty",
        f"{due_today['Shortage'].clip(lower=0).sum():,.0f}"
    )

# Compact table for planners
display_df = due_today[
    [
        "PD Eff.Dte",
        "Material",
        "Material Description",
        "Bklg.Qty",
        "Stock",
        "ShipToCtry"
    ]
].sort_values(
    by="PD Eff.Dte",
    ascending=True
)

st.subheader("Due Today / Overdue Orders")

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "PD Eff.Dte": st.column_config.DateColumn(
            "Due Date",
            width="small"
        ),
        "Material": st.column_config.TextColumn(
            "Material",
            width="small"
        ),
        "Material Description": st.column_config.TextColumn(
            "Material Description",
            width="large"
        ),
        "Bklg.Qty": st.column_config.NumberColumn(
            "Qty",
            width="small"
        ),
        "Stock": st.column_config.NumberColumn(
            "Stock",
            width="small"
        ),
        "ShipToCtry": st.column_config.TextColumn(
            "Country",
            width="small"
        ),
    },
    height=900
)
