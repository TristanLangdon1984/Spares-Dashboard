import streamlit as st
import pandas as pd

from utils.value_stream import build_filtered_df
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

df = build_filtered_df()

base_df = build_filtered_df()

filtered_df = base_df.copy()

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

future_orders = filtered_df[
    filtered_df["Adjusted Target Pack Date"]
    .dt.normalize()
    > week_end
].copy()

# KPIS

k1, k2, k3, k4 = st.columns(4)

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

k4.metric(
    "Future Orders",
    len(future_orders)
)

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Due Today",
        "Next 7 Days",
        "Backlog Recovery",
        "Future Orders",
        "Shortage Review"
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
        width="stretch",
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
        width="stretch",
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
        width="stretch",
        hide_index=True,
        height=900
    )

with tab4:

    st.subheader("Future Orders")

    st.metric(
        "Order Lines",
        len(future_orders)
    )

    st.dataframe(
        build_display_df(future_orders),
        width="stretch",
        hide_index=True,
        height=900
    )
with tab5:

    st.subheader("Shortage Review")

    shortage_df = filtered_df[
        filtered_df["Status"] == "❌ Short"
    ].copy()

    if len(shortage_df) == 0:

        st.success("No shortages found")

    else:

        shortage_summary = (
            shortage_df
            .groupby(
                [
                    "Material",
                    "Material Description"
                ],
                as_index=False
            )
            .agg(
                Orders=("Document", "nunique"),
                Total_Qty=("Qty", "sum"),
                Stock=("StockQty", "max")
            )
        )

        shortage_summary["Shortage"] = (
            shortage_summary["Total_Qty"]
            - shortage_summary["Stock"]
        )

        shortage_summary = shortage_summary.sort_values(
            by="Shortage",
            ascending=False
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Short Materials",
            shortage_summary["Material"].nunique()
        )

        c2.metric(
            "Affected Orders",
            shortage_df["Document"].nunique()
        )

        c3.metric(
            "Total Shortage Qty",
            int(
                shortage_summary["Shortage"]
                .clip(lower=0)
                .sum()
            )
        )

        st.write("### Shortage Summary")

        st.dataframe(
            shortage_summary,
            width="stretch",
            hide_index=True,
            height=400
        )

        st.divider()

        selected_material = st.selectbox(
            "Select Material for Order Detail",
            shortage_summary["Material"].tolist()
        )

        material_detail = shortage_df[
            shortage_df["Material"]
            == selected_material
        ].copy()

        detail_df = material_detail[
            [
                "Document",
                "Material",
                "Material Description",
                "ShipToCtry",
                "Qty",
                "StockQty",
                "Adjusted Target Pack Date",
                "PD Eff.Dte",
                "Status"
            ]
        ].copy()

        detail_df.columns = [
            "Order",
            "Material",
            "Description",
            "Country",
            "Qty",
            "Stock",
            "Pack Date",
            "PD Eff Date",
            "Status"
        ]

        detail_df["Pack Date"] = pd.to_datetime(
            detail_df["Pack Date"],
            errors="coerce"
        ).dt.strftime("%d/%m/%Y")

        detail_df["PD Eff Date"] = pd.to_datetime(
            detail_df["PD Eff Date"],
            errors="coerce"
        ).dt.strftime("%d/%m/%Y")

        detail_df = detail_df.fillna("")

        st.write(
            f"### Orders Impacted by {selected_material}"
        )

        st.dataframe(
            detail_df,
            width="stretch",
            hide_index=True,
            height=600
        )
