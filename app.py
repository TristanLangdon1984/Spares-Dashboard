import streamlit as st
import pandas as pd

st.set_page_config(page_title='SAP Spares Dashboard', layout='wide')

st.title('SAP Spares Control Tower')

uploaded_file = 'SAP Spares Report Generator.xlsm'

try:
    xl = pd.ExcelFile(uploaded_file, engine='openpyxl')
    st.success(f'Workbook loaded: {uploaded_file}')
    st.write('Sheets:', xl.sheet_names)

    sheet = st.selectbox('Select Sheet', xl.sheet_names)
    df = pd.read_excel(uploaded_file, sheet_name=sheet, engine='openpyxl')

    st.subheader(sheet)
    st.dataframe(df)
except Exception as e:
    st.error(f'Could not load workbook: {e}')
