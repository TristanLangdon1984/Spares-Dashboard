import streamlit as st
import pandas as pd

from utils.loader import load_backlog
from config.excluded_parts import EXCLUDED_PARTS
from config.c4c_parts import C4C_PARTS

st.set_page_config(
    page_title="Next 7 Days",
    layout="wide"
)

st.title("Next 7 Days")


def classify_product(material):

    material = str(material).upper().strip()

    # PRIME
    if (
        material.startswith("S091.")
        or material.startswith("91.")
    ):
        return "PRIME"

    # BOND
    if (
        material.startswith("S21.")
        or material.startswith("21.")
        or material.startswith("S49.")
        or material.startswith("49.")
    ):
        return "BOND"

    # PELORIS
    if (
        material.startswith("S26.")
        or material.startswith("26.")
        or material.startswith("S45.")
        or material.startswith("45.")
    ):
        return "PELORIS"

    # TBE
    if (
        material.startswith("S33.")
        or material.startswith("33.")
    ):
        return "TBE"

    return "OTHER"


# -----------------------
# LOAD DATA
# -----------------------

df = load_backlog()

# Remove fully excluded materials
df = df[
    ~df["Material"]
    .astype(str)
    .str.strip()
    .isin(EXCLUDED_PARTS)
]

# Capture C4C materials
c4c_df = df[
    df["Material"]
    .astype(str)
    .str.strip()
    .isin(C4C_PARTS)
].copy()

# Remove C4C from operational queue
df = df[
    ~df["Material"]
    .astype(str)
    .str.strip()
    .isin(C4C_PARTS)
]

# -----------------------
# DATES
# -----------------------

df["Doc. Date"] = pd.to_datetime(
    df["Doc. Date"],
    dayfirst=True,
    errors="coerce"
)

df["PD Eff.Dte"] = pd.to_datetime(
    df["PD Eff.Dte"],
    dayfirst=True,
    errors="coerce"
)

# -----------------------
# QTY
# SAP Export:
# 3,000 = 3
# -----------------------

df["Qty"] = (
    df["Bklg.Qty"]
    .astype(str)
    .str.replace(",", ".", regex=False)
)

df["Qty"] = (
    pd.to_numeric(
        df["Qty"],
        errors="coerce"
    )
    .fillna(0)
    .astype(int)
)

# -----------------------
# STOCK
# -----------------------

df["StockQty"] = (
    df["Stock"]
    .astype(str)
    .str.replace(",", ".", regex=False)
)

df["StockQty"] = (
    pd.to_numeric(
        df["StockQty"],
        errors="coerce"
    )
    .fillna(0)
    .astype(int)
)

# -----------------------
# PRODUCT CLASSIFICATION
# -----------------------

df["Product"] = (
    df["Material"]
    .astype(str)
    .str.strip()
    .apply(classify_product)
)

# -----------------------
# NEXT 7 DAYS
# Based on PD Eff.Dte
# -----------------------

today = pd.Timestamp.today().normalize()

