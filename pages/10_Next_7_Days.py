import streamlit as st
import pandas as pd

from utils.loader import load_backlog

st.title("Next 7 Days Diagnostic")


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


df = load_backlog()

df["Doc. Date"] = pd.to_datetime(
    df["Doc. Date"],
    dayfirst=True,
    errors="coerce"
)

df["Adjusted Target Pack Date"] = (
    df["Doc. Date"]
    .apply(lambda x: add_business_days(x, 3))
)

today = pd.Timestamp.today().normalize()
week_end = today + pd.Timedelta(days=7)

st.write("Today")
st.write(today)

st.write("Week End")
st.write(week_end)

st.write("Min Adjusted Date")
st.write(df["Adjusted Target Pack Date"].min())

st.write("Max Adjusted Date")
st.write(df["Adjusted Target Pack Date"].max())

st.write("Next 50 Records")

st.dataframe(
    df[
        [
            "Doc. Date",
            "Adjusted Target Pack Date",
            "Material",
            "Material Description"
        ]
    ]
    .sort_values("Adjusted Target Pack Date")
    .tail(50)
)

next_7 = df[
    (
        df["Adjusted Target Pack Date"].dt.normalize()
        > today
    )
    &
    (
        df["Adjusted Target Pack Date"].dt.normalize()
        <= week_end
    )
]

st.write("Records Found")

st.write(len(next_7))
