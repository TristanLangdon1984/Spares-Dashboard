import streamlit as st
import pandas as pd

from utils.loader import load_mb51

st.set_page_config(
    page_title="Consumption Analytics",
    layout="wide"
)

st.title("Consumption Analytics")

df = load_mb51()

st.write(df.columns.tolist())

# ----------------------------
# DATE CLEANUP
# ----------------------------

date_column = "Pstng Date"

if date_column in df.columns:

    df[date_column] = pd.to_datetime(
        df[date_column],
        dayfirst=True,
        errors="coerce"
    )

# ----------------------------
# QUANTITY CLEANUP
# ----------------------------

qty_column = "Quantity"

if qty_column in df.columns:

    df[qty_column] = pd.to_numeric(
        df[qty_column]
        .astype(str)
        .str.replace(",", ".", regex=False),
        errors="coerce"
    ).fillna(0)

# ----------------------------
# FILTERS
# ----------------------------

f1, f2 = st.columns(2)

with f1:

    if "MvT" in df.columns:

        movement_types = sorted(
            df["MvT"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )

        movement_type = st.selectbox(
            "Movement Type",
            ["ALL"] + movement_types
        )

    else:

        movement_type = "ALL"

with f2:

    if "Plant" in df.columns:

        plants = sorted(
            df["Plant"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )

        plant = st.selectbox(
            "Plant",
            ["ALL"] + plants
        )

    else:

        plant = "ALL"

filtered_df = df.copy()

if movement_type != "ALL":

    filtered_df = filtered_df[
        filtered_df["MvT"].astype(str)
        == movement_type
    ]

if plant != "ALL":

    filtered_df = filtered_df[
        filtered_df["Plant"].astype(str)
        == plant
    ]

# ----------------------------
# KPIs
# ----------------------------

total_qty = (
    filtered_df[qty_column].sum()
    if qty_column in filtered_df.columns
    else 0
)

materials = (
    filtered_df["Material"]
    .nunique()
    if "Material" in filtered_df.columns
    else 0
)

transactions = len(filtered_df)

k1, k2, k3 = st.columns(3)

k1.metric(
    "Consumption Qty",
    f"{total_qty:,.0f}"
)

k2.metric(
    "Materials Consumed",
    materials
)

k3.metric(
    "Transactions",
    transactions
)

# ----------------------------
# MONTHLY TREND
# ----------------------------

st.subheader(
    "Monthly Consumption Trend"
)

if (
    date_column in filtered_df.columns
    and qty_column in filtered_df.columns
):

    trend_df = filtered_df.copy()

    trend_df["Month"] = (
        trend_df[date_column]
        .dt.to_period("M")
        .astype(str)
    )

    trend_summary = (
        trend_df
        .groupby(
            "Month",
            as_index=False
        )[qty_column]
        .sum()
    )

    st.line_chart(
        trend_summary.set_index("Month")
    )

# ----------------------------
# TOP MATERIALS
# ----------------------------

st.subheader(
    "Top Consumed Materials"
)

if (
    "Material" in filtered_df.columns
    and qty_column in filtered_df.columns
):

    top_materials = (
        filtered_df
        .groupby(
            "Material",
            as_index=False
        )[qty_column]
        .sum()
        .sort_values(
            qty_column,
            ascending=False
        )
        .head(25)
    )

    st.dataframe(
        top_materials,
        width="stretch",
        hide_index=True
    )

# ----------------------------
# MATERIAL DETAILS
# ----------------------------

st.subheader(
    "Material Detail"
)

if "Material" in filtered_df.columns:

    materials_list = sorted(
    filtered_df["Material"]
    .dropna()
    .astype(str)
    .str.strip()
    .unique()
    .tolist()
)

    selected_material = st.selectbox(
        "Select Material",
        materials_list
    )
    
        selected_material = st.selectbox(
            "Select Material",
            materials_list
        )
    
        material_df = filtered_df[
            filtered_df["Material"]
            .astype(str)
            == selected_material
    ]

    st.dataframe(
        material_df,
        width="stretch",
        hide_index=True,
        height=500
    )

# ----------------------------
# RAW DATA
# ----------------------------

with st.expander(
    "Show Raw MB51 Data"
):

    st.dataframe(
        filtered_df,
        width="stretch",
        hide_index=True,
        height=600
    )
