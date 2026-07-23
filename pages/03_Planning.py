import streamlit as st

st.set_page_config(
    page_title="Planning",
    layout="wide"
)

st.title("Planning")

# Global Filters

f1, f2, f3, f4, f5 = st.columns(5)

with f1:
    st.selectbox(
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
    st.selectbox(
        "Delivery Status",
        [
            "ALL",
            "✅ Can Deliver",
            "❌ Short"
        ]
    )

with f3:
    st.checkbox(
        "Exclude Instrument Orders"
    )

with f4:
    st.checkbox(
        "Exclude DS9800"
    )

with f5:
    st.checkbox(
        "Exclude Obsolete"
    )

# KPI ROW

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Short Materials",
    0
)

k2.metric(
    "Affected Orders",
    0
)

k3.metric(
    "Future Demand Qty",
    0
)

k4.metric(
    "Countries Impacted",
    0
)

# TABS

tab1, tab2, tab3 = st.tabs(
    [
        "Shortage Review",
        "Supply Risk",
        "Future Demand"
    ]
)

# ------------------------
# SHORTAGE REVIEW
# ------------------------

with tab1:

    st.subheader(
        "Shortage Review"
    )

    st.info(
        "Material shortages grouped by material."
    )

# ------------------------
# SUPPLY RISK
# ------------------------

with tab2:

    st.subheader(
        "Supply Risk"
    )

    st.info(
        "Prioritised risk assessment by customers impacted and shortage quantity."
    )

# ------------------------
# FUTURE DEMAND
# ------------------------

with tab3:

    st.subheader(
        "Future Demand"
    )

    st.info(
        "Demand beyond the next 7 days."
    )
