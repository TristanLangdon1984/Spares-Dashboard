import streamlit as st
import pandas as pd

from utils.loader import load_backlog
from config.excluded_parts import EXCLUDED_PARTS
from config.c4c_parts import C4C_PARTS
from config.obsolete_parts import OBSOLETE_PARTS

try:
    from config.excluded_prefixes import EXCLUDED_PREFIXES
except ImportError:
    EXCLUDED_PREFIXES = []

st.set_page_config(
    page_title="Backlog Recovery",
    layout="wide"
)

st.title("Backlog Recovery")

INSTRUMENT_PARTS = [
    "21.2201",
    "21.2821",
    "45.0001",
    "45.0005",
    "49.0051",
    "49.1501",
    "91.0021"
]


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

    if material.startswith("B"):
        return "TSB"

    if (
        material.startswith("98.")
        or material.startswith("S98.")
        or material.startswith("9800")
        or material.startswith("DS9800")
    ):
        return "DS9800"

    if (
        material.startswith("S091.")
        or material.startswith("91.")
    ):
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


# LOAD DATA

df = load_backlog()

df["Material"] = (
    df["Material"]
    .astype(str)
    .str.strip()
)

# REMOVE EXCLUDED PARTS

df = df[
    ~df["Material"].isin(EXCLUDED_PARTS)
]

# REMOVE C4C PARTS

df = df[
    ~df["Material"].isin(C4C_PARTS)
]

# REMOVE EXCLUDED PREFIXES

for prefix in EXCLUDED_PREFIXES:

    df = df[
        ~df["Material"].str.startswith(prefix)
    ]

# DATES

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

def subtract_business_days(start_date, business_days):

    if pd.isna(start_date):
        return pd.NaT

    current_date = start_date
    days_removed = 0

    while days_removed < business_days:

        current_date = current_date - pd.Timedelta(days=1)

        if current_date.weekday() < 5:
            days_removed += 1

    return current_date


# Initial pack date = Doc Date + 3 working days

initial_pack_date = df["Doc. Date"].apply(
    lambda x: add_business_days(x, 3)
)

df["Adjusted Target Pack Date"] = initial_pack_date

# Compare to PD Eff Date

date_gap = (
    df["PD Eff.Dte"]
    - initial_pack_date
).dt.days

# If PD Eff Date is more than 2 days later than the pack date
# then work backwards 3 business days from PD Eff Date

needs_replan = date_gap > 2

df.loc[
    needs_replan,
    "Adjusted Target Pack Date"
] = df.loc[
    needs_replan,
    "PD Eff.Dte"
].apply(
    lambda x: subtract_business_days(x, 3)
)

# QTY

df["Qty"] = pd.to_numeric(
    df["Bklg.Qty"]
    .astype(str)
    .str.replace(",", ".", regex=False),
    errors="coerce"
).fillna(0)

# STOCK

df["StockQty"] = pd.to_numeric(
    df["Stock"]
    .astype(str)
    .str.replace(",", ".", regex=False),
    errors="coerce"
).fillna(0)

# PRODUCT

df["Product"] = df["Material"].apply(
    classify_product
)

# STATUS

df["Status"] = "❌ Short"

df.loc[
    df["StockQty"] >= df["Qty"],
    "Status"
] = "✅ Can Deliver"

df["Shortage"] = (
    df["Qty"] - df["StockQty"]
)

# INSTRUMENT ORDERS

instrument_documents = set(
    df.loc[
        df["Material"].isin(INSTRUMENT_PARTS),
        "Document"
    ]
)

df["Instrument"] = (
    df["Document"]
    .isin(instrument_documents)
)

# OBSOLETE ORDERS

obsolete_documents = set(
    df.loc[
        df["Material"].isin(OBSOLETE_PARTS),
        "Document"
    ]
)

df["Obsolete"] = (
    df["Document"]
    .isin(obsolete_documents)
)

# BACKLOG WINDOW

today = pd.Timestamp.today().normalize()

three_months_ago = today - pd.DateOffset(months=3)

backlog = df[
    (
        df["Adjusted Target Pack Date"].dt.normalize()
        < today
    )
    &
    (
        df["Adjusted Target Pack Date"].dt.normalize()
        >= three_months_ago
    )
].copy()

# FILTERS

f1, f2, f3, f4, f5 = st.columns(5)

with f1:

    product_filter = st.radio(
        "Product Family",
        [
            "ALL",
            "BOND",
            "PRIME",
            "PELORIS",
            "TBE",
            "DS9800",
            "TSB",
            "OTHER"
        ],
        horizontal=True
    )

with f2:

    status_filter = st.radio(
        "Delivery Status",
        [
            "ALL",
            "✅ Can Deliver",
            "❌ Short"
        ],
        horizontal=True
    )

with f3:

    exclude_instruments = st.checkbox(
        "Exclude Instrument Orders"
    )

with f4:

    exclude_ds9800 = st.checkbox(
        "Exclude DS9800"
    )

with f5:

    exclude_obsolete = st.checkbox(
        "Exclude Obsolete"
    )

# APPLY FILTERS

if product_filter != "ALL":

    backlog = backlog[
        backlog["Product"] == product_filter
    ]

if status_filter != "ALL":

    backlog = backlog[
        backlog["Status"] == status_filter
    ]

if exclude_instruments:

    backlog = backlog[
        ~backlog["Instrument"]
    ]

if exclude_ds9800:

    backlog = backlog[
        backlog["Product"] != "DS9800"
    ]

if exclude_obsolete:

    backlog = backlog[
        ~backlog["Obsolete"]
    ]

# KPI CARDS

c1, c2, c3, c4, c5, c6, c7, c8 = st.columns(8)

c1.metric("Backlog Lines", len(backlog))

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
    int(backlog["Shortage"].clip(lower=0).sum())
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

c7.metric(
    "Instrument Orders",
    backlog.loc[
        backlog["Instrument"],
        "Document"
    ].nunique()
)

c8.metric(
    "Obsolete Orders",
    backlog.loc[
        backlog["Obsolete"],
        "Document"
    ].nunique()
)

# TABLE

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
        "Status",
        "Instrument",
        "Obsolete",
        "ShipToCtry",
        "Plnt",
        "Express De"
    ]
].copy()

display_df.columns = [
    "Doc Date",
    "Pack Date",
    "PD Eff Date",
    "Order",
    "Material",
    "Description",
    "Qty",
    "Stock",
    "Status",
    "Instrument",
    "Obsolete",
    "Country",
    "Plant",
    "Express"
]

display_df = display_df.sort_values(
    by=["Pack Date", "Material"]
)

# REMOVE TIME FROM DATES

display_df["Doc Date"] = pd.to_datetime(
    display_df["Doc Date"]
).dt.strftime("%d/%m/%Y")

display_df["Pack Date"] = pd.to_datetime(
    display_df["Pack Date"]
).dt.strftime("%d/%m/%Y")

display_df["PD Eff Date"] = pd.to_datetime(
    display_df["PD Eff Date"]
).dt.strftime("%d/%m/%Y")

st.subheader("Backlog Recovery")

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    height=900
)
