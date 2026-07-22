import streamlit as st
import pandas as pd

st.title("SAP Workbook Diagnostic")

FILE = "data/SAP Spares Report Generator.xlsm"

try:
    xl = pd.ExcelFile(
        FILE,
        engine="openpyxl"
    )

    st.success("Workbook loaded successfully")

    st.subheader("Available Sheets")
    st.write(xl.sheet_names)

    sheet = st.selectbox(
        "Choose Sheet",
        xl.sheet_names
    )

    df = pd.read_excel(
        FILE,
        sheet_name=sheet,
        engine="openpyxl",
        header=None
    )

    st.subheader(f"Preview: {sheet}")
    st.dataframe(df.head(30))

except Exception as e:
    st.error(f"Error: {e}")
