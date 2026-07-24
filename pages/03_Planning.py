import streamlit as st
import pandas as pd

from utils.value_stream import (
    build_filtered_df
)

st.set_page_config(
    page_title="Planning",
    layout="wide"
)

st.title("Planning")

filtered_df = build_filtered_df()

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

released_orders = len(
    filtered_df[
        filtered_df["DL"]
        .fillna("")
        .astype(str)
        .str.upper()
        .str.strip()
        == "X"
    ]
)

k1, k2, k3 = st.columns(3)

k1.metric(
    "Late Orders",
    late_orders
)

k2.metric(
    "Short Orders",
    short_orders
)

k3.metric(
    "Released Orders",
    released_orders
)

# TABS

tab1, tab2, tab3 = st.tabs(
    [
        "Shortage Review",
        "Supply Risk",
        "Future Demand"
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
                Demand_Qty=("Qty", "sum"),
                Stock=("StockQty", "max")
            )
        )

        shortage_summary["Shortage_Qty"] = (
            shortage_summary["Demand_Qty"]
            - shortage_summary["Stock"]
        )

        shortage_summary = shortage_summary.sort_values(
            by="Shortage_Qty",
            ascending=False
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

        supply_risk["Risk_Level"] = "LOW"

        supply_risk.loc[
            supply_risk["Shortage_Qty"] > 5,
            "Risk_Level"
        ] = "MEDIUM"

        supply_risk.loc[
            supply_risk["Shortage_Qty"] > 10,
            "Risk_Level"
        ] = "HIGH"

        supply_risk.loc[
            supply_risk["Shortage_Qty"] > 20,
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

    today = pd.Timestamp.today().normalize()

    week_end = (
        today +
        pd.Timedelta(days=7)
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
