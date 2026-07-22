import pandas as pd
WORKBOOK='data/SAP Spares Report Generator.xlsm'

def load_metrics():
    return pd.read_excel(WORKBOOK,sheet_name=0,engine='openpyxl')

def load_parts():
    return pd.read_excel(WORKBOOK,sheet_name=1,engine='openpyxl')

def load_backlog():
    return pd.read_excel(WORKBOOK,sheet_name=2,engine='openpyxl')
