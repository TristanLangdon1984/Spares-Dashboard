import streamlit as st

from utils.file_loader import (
    get_latest_backlog,
    get_latest_mb51
)

st.title("SAP File Check")

col1, col2 = st.columns(2)

with col1:

    try:
        backlog = get_latest_backlog()

        st.success("Backlog File Found")

        st.code(str(backlog))

    except Exception as e:

        st.error(e)

with col2:

    try:
        mb51 = get_latest_mb51()

        st.success("MB51 File Found")

        st.code(str(mb51))

    except Exception as e:

        st.error(e)
