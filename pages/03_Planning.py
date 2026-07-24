import streamlit as st
import pandas as pd

from utils.value_stream import build_filtered_df

st.set_page_config(
    page_title="Planning",
    layout="wide"
)

st.title("Planning")

filtered_df = build_filtered_df()

# --------------------------------
# RELEASE FILTER
# --------------------------------

released_filter = st.selectbox(
    "Released Status",
    [
        "ALL",
        "Released",
        "Not Released"
    ]
)

if "DL" in filtered_df.columns:

    dl_flag = (
        filtered_df["DL"]
        .fillna("")
        .astype(str)
        .str.upper()
        .str.strip()
    )

    if released_filter == "Released":

        filtered_df = filtered_df[
            dl_flag == "X"
        ]

    elif released_filter == "Not Released":

        filtered_df = filtered_df[
            dl_flag != "X"
        ]

# --------------------------------
# KPIS
# --------------------------------

today = pd.Timestamp.today().normalize()

late_orders = len(
    filtered_df[
        filtered_df["Adjusted Target Pack Date"]
        < today
    ]
)

short_orders = len(
    filtered_df[
        filtered_df["Status"]
        == "❌ Short"
    ]
)

released_orders = 0

if "DL" in filtered_df.columns:

    released_orders = len(
        filtered_df[
            dl_flag == "X"
        ]
    )

due_today = len(
    filtered_df[
        filtered_df[
            "Adjusted Target Pack Date"
        ].dt.normalize()
        == today
    ]
)

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Late Orders",
    late_orders
)

k2.metric(
    "Orders Due Today",
    due_today
)

k3.metric(
    "Short Orders",
    short_orders
)

k4.metric(
    "Released Orders",
    released_orders
)

# --------------------------------
# TABS
# --------------------------------

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Shortage Review",
        "Supply Risk",
        "Future Demand",
        "Planner Queue"
    ]
)

# --------------------------------
# SHORTAGE REVIEW
# --------------------------------

with tab1:

    st.subheader("Shortage Review")

    shortage_df = filtered_df[
        filtered_df["Status"] == "❌ Short"
    ].copy()

    if len(shortage_df) == 0:

        st.success(
            "No shortages found"
        )

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
                Demand_Qty=("Qty", "sum"),
                Stock=("StockQty", "max"),
                Earliest_Pack_Date=(
                    "Adjusted Target Pack Date",
                    "min"
                )
            )
        )

        shortage_summary["Shortage_Qty"] = (
            shortage_summary["Demand_Qty"]
            - shortage_summary["Stock"]
        )

        shortage_summary = shortage_summary.sort_values(
            by="Earliest_Pack_Date"
        )

        st.dataframe(
            shortage_summary,
            width="stretch",
            hide_index=True,
            height=500
        )

        selected_material = st.selectbox(
            "Select Material",
            shortage_summary["Material"].tolist()
        )

        material_orders = shortage_df[
            shortage_df["Material"]
            == selected_material
        ]

        st.write("### Impacted Orders")

        st.dataframe(
            material_orders,
            width="stretch",
            hide_index=True,
            height=500
        )

# --------------------------------
# SUPPLY RISK
# --------------------------------

with tab2:

    st.subheader("Supply Risk")

    risk_df = filtered_df[
        filtered_df["Status"] == "❌ Short"
    ].copy()

    if len(risk_df) == 0:

        st.success(
            "No supply risks identified"
        )

    else:

        supply_risk = (
            risk_df
            .groupby(
                [
                    "Material",
                    "Material Description"
                ],
                as_index=False
            )
            .agg(
                Orders=("Document", "nunique"),
                Countries=("ShipToCtry", "nunique"),
                Demand_Qty=("Qty", "sum"),
                Stock=("StockQty", "max"),
                Earliest_Pack_Date=(
                    "Adjusted Target Pack Date",
                    "min"
                )
            )
        )

        supply_risk["Shortage_Qty"] = (
            supply_risk["Demand_Qty"]
            - supply_risk["Stock"]
        )

        days_to_pack = (
            supply_risk["Earliest_Pack_Date"]
            - today
        ).dt.days

        supply_risk["Risk_Level"] = "LOW"

        supply_risk.loc[
            days_to_pack <= 14,
            "Risk_Level"
        ] = "MEDIUM"

        supply_risk.loc[
            days_to_pack <= 7,
            "Risk_Level"
        ] = "HIGH"

        supply_risk.loc[
            days_to_pack <= 3,
            "Risk_Level"
        ] = "CRITICAL"

        supply_risk["Earliest_Pack_Date"] = (
            pd.to_datetime(
                supply_risk["Earliest_Pack_Date"]
            )
            .dt.strftime("%d/%m/%Y")
        )

        supply_risk = supply_risk.sort_values(
            by="Shortage_Qty",
            ascending=False
        )

        st.dataframe(
            supply_risk,
            width="stretch",
            hide_index=True,
            height=700
        )

# --------------------------------
# FUTURE DEMAND
# --------------------------------

with tab3:

    st.subheader("Future Demand")

    week_end = (
        today
        + pd.Timedelta(days=7)
    )

    future_orders = filtered_df[
        filtered_df[
            "Adjusted Target Pack Date"
        ].dt.normalize()
        > week_end
    ].copy()

    if len(future_orders) == 0:

        st.info(
            "No future demand."
        )

    else:

        future_summary = (
            future_orders
            .groupby(
                [
                    "Product",
                    "Material",
                    "Material Description"
                ],
                as_index=False
            )
            .agg(
                Orders=("Document", "nunique"),
                Demand_Qty=("Qty", "sum")
            )
        )

        future_summary = (
            future_summary
            .sort_values(
                by="Demand_Qty",
                ascending=False
            )
        )

        st.write(
            "### Material Demand"
        )

        st.dataframe(
            future_summary,
            width="stretch",
            hide_index=True,
            height=500
        )

        st.write(
            "### Detailed Future Orders"
        )

        st.dataframe(
            future_orders,
            width="stretch",
            hide_index=True,
            height=700
        )

# --------------------------------
# PLANNER QUEUE
# --------------------------------

with tab4:

    st.subheader(
        "Planner Queue"
    )

    planner_df = filtered_df[
        filtered_df["Status"]
        == "❌ Short"
    ].copy()

    planner_df = planner_df.sort_values(
        by="Adjusted Target Pack Date"
    )

    columns = [
        "Document",
        "Material",
        "Material Description",
        "Qty",
        "StockQty",
        "Adjusted Target Pack Date",
        "PD Eff.Dte",
        "ShipToCtry"
    ]

    if "DL" in planner_df.columns:
        columns.append("DL")

    available_columns = [
        col
        for col in columns
        if col in planner_df.columns
    ]

    st.dataframe(
        planner_df[
            available_columns
        ],
        width="stretch",
        hide_index=True,
        height=800
    )
