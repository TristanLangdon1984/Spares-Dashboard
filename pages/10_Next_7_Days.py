import streamlit as st
import pandas as pd

from utils.loader import load_backlog

st.set_page_config(
    page_title="Next 7 Days",
    layout="wide"
)

st.title("Next 7 Days")

df = load_backlog()

df["Doc. Date"] = pd.to_datetime(
    df["Doc. Date"],
    dayfirst=True,
    errors="coerce"
)

today = pd.Timestamp.today().normalize()
week_end = today + pd.Timedelta(days=7)

st.write("Today:", today)
st.write("Week End:", week_end)

display_df = df[
    [
        "Doc. Date",
        "Material",
        "Material Description",
        "Bklg.Qty",
        "Stock"
    ]
].copy()

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)
