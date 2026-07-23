import streamlit as st

st.set_page_config(
    page_title="Value Stream",
    layout="wide"
)

st.title("Value Stream")

st.markdown("### Global Filters")

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

tab1, tab2, tab3 = st.tabs(
    [
        "Due Today",
        "Next 7 Days",
        "Backlog Recovery"
    ]
)

with tab1:

    st.subheader("Due Today")

    st.info(
        "Due Today content will go here"
    )

with tab2:

    st.subheader("Next 7 Days")

    st.info(
        "Next 7 Days content will go here"
    )

with tab3:

    st.subheader("Backlog Recovery")

    st.info(
        "Backlog Recovery content will go here"
    )
