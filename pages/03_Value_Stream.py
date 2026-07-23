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
    page_title="Value Stream",
    layout="wide"
)

st.title("Value Stream")

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

# REMOVE EXCLUDED

df = df[
    ~df["Material"].isin(EXCLUDED_PARTS)
]

df = df[
    ~df["Material"].isin(C4C_PARTS)
]

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

initial_pack_date = df["Doc. Date"].apply(
    lambda x: add_business_days(x, 3)
)

df["Adjusted Target Pack Date"] = initial_pack_date

date_gap = (
    df["PD Eff.Dte"] -
    initial_pack_date
).dt.days

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

# INSTRUMENTS

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

# OBSOLETE

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

# GLOBAL FILTERS

f1, f2, f3, f4, f5 = st.columns(5)

with f1:

    product_filter = st.selectbox(
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
        ]
    )

with f2:

    status_filter = st.selectbox(
        "Delivery Status",
        [
            "ALL",
            "✅ Can Deliver",
            "❌ Short"
        ]
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

filtered_df = df.copy()

if product_filter != "ALL":

    filtered_df = filtered_df[
        filtered_df["Product"] == product_filter
    ]

if status_filter != "ALL":

    filtered_df = filtered_df[
        filtered_df["Status"] == status_filter
    ]

if exclude_instruments:

    filtered_df = filtered_df[
        ~filtered_df["Instrument"]
    ]

if exclude_ds9800:

    filtered_df = filtered_df[
        filtered_df["Product"] != "DS9800"
    ]

if exclude_obsolete:

    filtered_df = filtered_df[
        ~filtered_df["Obsolete"]
    ]

# DATE BUCKETS

today = pd.Timestamp.today().normalize()

week_end = today + pd.Timedelta(days=7)

three_months_ago = today - pd.DateOffset(months=3)

due_today = filtered_df[
    filtered_df["Adjusted Target Pack Date"]
    .dt.normalize()
    == today
]

next_7_days = filtered_df[
    (
        filtered_df["Adjusted Target Pack Date"]
        .dt.normalize()
        > today
    )
    &
    (
        filtered_df["Adjusted Target Pack Date"]
        .dt.normalize()
        <= week_end
    )
]

backlog = filtered_df[
    (
        filtered_df["Adjusted Target Pack Date"]
        .dt.normalize()
        < today
    )
    &
    (
        filtered_df["Adjusted Target Pack Date"]
        .dt.normalize()
        >= three_months_ago
    )
]

# KPIS

k1, k2, k3 = st.columns(3)

k1.metric(
    "Due Today",
    len(due_today)
)

k2.metric(
    "Next 7 Days",
    len(next_7_days)
)

k3.metric(
    "Backlog",
    len(backlog)
)

tab1, tab2, tab3 = st.tabs(
    [
        "Due Today",
        "Next 7 Days",
        "Backlog Recovery"
    ]
)


def build_display_df(source_df):

    display_df = source_df[
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
        by=[
            "Pack Date",
            "Material"
        ]
    )

    display_df["Doc Date"] = pd.to_datetime(
        display_df["Doc Date"]
    ).dt.strftime("%d/%m/%Y")

    display_df["Pack Date"] = pd.to_datetime(
        display_df["Pack Date"]
    ).dt.strftime("%d/%m/%Y")

    display_df["PD Eff Date"] = pd.to_datetime(
        display_df["PD Eff Date"]
    ).dt.strftime("%d/%m/%Y")

    return display_df


with tab1:

    st.subheader("Orders Due Today")

    st.metric(
        "Order Lines",
        len(due_today)
    )

    st.dataframe(
        build_display_df(due_today),
        use_container_width=True,
        hide_index=True,
        height=900
    )

with tab2:

    st.subheader("Orders Due In Next 7 Days")

    st.metric(
        "Order Lines",
        len(next_7_days)
    )

    st.dataframe(
        build_display_df(next_7_days),
        use_container_width=True,
        hide_index=True,
        height=900
    )

with tab3:

    st.subheader("Backlog Recovery")

    st.metric(
        "Backlog Lines",
        len(backlog)
    )

    st.dataframe(
        build_display_df(backlog),
        use_container_width=True,
        hide_index=True,
        height=900
    )
