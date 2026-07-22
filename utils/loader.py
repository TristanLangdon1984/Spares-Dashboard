import pandas as pd

FILE = "data/SAP Spares Report Generator.xlsm"


def load_metrics():

    df = pd.read_excel(
        FILE,
        sheet_name="Cell Metric History",
        engine="openpyxl",
        header=1
    )

    return df


def load_parts():

    df = pd.read_excel(
        FILE,
        sheet_name="Part Timings",
        engine="openpyxl"
    )

    return df


def load_backlog():

    df = pd.read_excel(
        FILE,
        sheet_name="ZVREP386 - 3013BACKLOG1",
        engine="openpyxl"
    )

    return df
