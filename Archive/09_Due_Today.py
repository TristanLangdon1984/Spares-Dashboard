import streamlit as st
import pandas as pd

from utils.loader import load_backlog
from config.excluded_parts import EXCLUDED_PARTS
from config.c4c_parts import C4C_PARTS

st.set_page_config(
    page_title="Due Today",
    layout="wide"
)

st.title("Due Today")


def add_business_days(start_date, business_days):

    if pd.isna(start_date):
        return pd.NaT

    current_date = start_date
    days_added = 0

    while days_added < business_days:

        current_date = current_date + pd.Timedelta(days=1)

        if current_date.weekday() < 5:
            days_added += 1

    return current_date


def classify_product(material):

    material = str(material).upper().strip()

    if material.startswith("S091.") or material.startswith("91."):
        return "PRIME"

    if material.startswith("S21.") or material.startswith("21."):
        return "BOND"

    if material.startswith("S49.") or material.startswith("49."):
        return "BOND"

    if material.startswith("S26.") or material.startswith("26."):
        return "PELORIS"

    if material.startswith("S45.") or material.startswith("45."):
        return "PELORIS"

