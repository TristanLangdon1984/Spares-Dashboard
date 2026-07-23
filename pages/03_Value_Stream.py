import streamlit as st
import pandas as pd

from utils.value_stream import build_filtered_df

st.set_page_config(
    page_title="Value Stream",
    layout="wide"
)

st.title("Value Stream")

# LOAD DATA

df = build_filtered_df()

# GLOBAL FILTERS

f1, f2, f3, f4, f5, f6 = st.columns(6)

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

with f6:

    released_filter = st.selectbox(
        "Released",
        [
            "ALL",
            "✅ Released",
            "❌ Not Released"
        ]
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
    
if "DL" in filtered_df.columns:

    dl_flag = (
        filtered_df["DL"]
        .fillna("")
        .astype(str)
        .str.upper()
        .str.strip()
    )

    if released_filter == "✅ Released":

        filtered_df = filtered_df[
            dl_flag != "X"
        ]

    elif released_filter == "❌ Not Released":

        filtered_df = filtered_df[
            dl_flag == "X"
        ]

# DYNAMIC SEARCH

search_text = st.text_input(
    "Search Material, Order or Description",
    placeholder="e.g. 21.2201, PM Kit, 50012345..."
)

if search_text:

    filtered_df = filtered_df[
        (
            filtered_df["Material"]
            .astype(str)
            .str.contains(
                search_text,
                case=False,
                na=False
            )
        )
        |
        (
            filtered_df["Document"]
            .astype(str)
            .str.contains(
                search_text,
                case=False,
                na=False
            )
        )
        |
        (
            filtered_df["Material Description"]
            .astype(str)
            .str.contains(
                search_text,
                case=False,
                na=False
            )
        )
    ]

# DATE BUCKETS

today = pd.Timestamp.today().normalize()

week_end = today + pd.Timedelta(days=7)

three_months_ago = (
    today - pd.DateOffset(months=3)
)

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

    required_columns = [
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
        "Plnt"
    ]

    display_df = source_df[
        required_columns
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
        "Plant"
    ]

    display_df = display_df.sort_values(
        by=[
            "Pack Date",
            "Material"
        ]
    )

    display_df["Doc Date"] = pd.to_datetime(
        display_df["Doc Date"],
        errors="coerce"
    ).dt.strftime("%d/%m/%Y")

    display_df["Pack Date"] = pd.to_datetime(
        display_df["Pack Date"],
        errors="coerce"
    ).dt.strftime("%d/%m/%Y")

    display_df["PD Eff Date"] = pd.to_datetime(
        display_df["PD Eff Date"],
        errors="coerce"
    ).dt.strftime("%d/%m/%Y")

    
ddisplay_df = display_df.fillna("")

display_df = display_df.astype(str)

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
