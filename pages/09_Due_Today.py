import streamlit as st
import pandas as pd

from utils.loader import load_backlog

st.set_page_config(
    page_title="Due Today",
    layout="wide"
)

st.title("Due Today")

# Load data
df = load_backlog()

# Convert date column
df["PD Eff.Dte"] = pd.to_datetime(
    df["PD Eff.Dte"],
    dayfirst=True,
    errors="coerce"
)

# Clean quantity column
df["Bklg.Qty"] = (
    df["Bklg.Qty"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .str.extract(r"([-]?\d*\.?\d+)")[0]
)

df["Bklg.Qty"] = pd.to_numeric(
    df["Bklg.Qty"],
    errors="coerce"
)

# Clean stock column
df["Stock"] = (
    df["Stock"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .str.extract(r"([-]?\d*\.?\d+)")[0]
)

df["Stock"] = pd.to_numeric(
    df["Stock"],
    errors="coerce"
)

# Today's date
today = pd.Timestamp.today().normalize()

# Due today or overdue
due_today = df[
    df["PD Eff.Dte"] <= today
].copy()

# Calculate shortages
due_today["Shortage"] = (
    due_today["Bklg.Qty"].fillna(0)
    - due_today["Stock"].fillna(0)
)

# KPI Row
col1, col2, col3, col4 = st.columns(4)

with col1:
