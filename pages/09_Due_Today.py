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
    added_days = 0

    while added_days < business_days:

        current_date = current_date + pd.Timedelta(days=1)

        if current_date.weekday() < 5:
            added_days += 1

    return current_date


