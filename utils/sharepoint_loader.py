import pandas as pd

def load_backlog():

    return pd.read_excel(
        "https://YOUR_SHAREPOINT_PATH/ZVREP386.xlsx"
    )

def load_mb51():

    return pd.read_excel(
        "https://YOUR_SHAREPOINT_PATH/MB51.xlsx"
    )
