import streamlit as st
import pandas as pd

from utils.loader import load_backlog

st.title("Due Today Diagnostic")

df = load_backlog()

df["PD Eff.Dte"] = pd.to_datetime(
    df["PD Eff.Dte"],
    dayfirst=True,
    errors="coerce"
)

today = pd.Timestamp.today().normalize()

st.write("Today:")
st.write(today)

st.write("Minimum PD Eff.Dte:")
st.write(df["PD Eff.Dte"].min())

st.write("Maximum PD Eff.Dte:")
st.write(df["PD Eff.Dte"].max())

st.write("Next 20 dates:")
st.dataframe(
    df[
        ["PD Eff.Dte", "Material", "Material Description"]
    ]
    .sort_values("PD Eff.Dte")
    .head(20)
)

st.write("Count Due Today:")

due_today = df[
    df["PD Eff.Dte"].dt.normalize() == today
]

st.write(len(due_today))
