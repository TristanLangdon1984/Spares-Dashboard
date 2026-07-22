import streamlit as st
import pandas as pd

from utils.loader import load_backlog

st.title("Due Today Debug")

df = load_backlog()

st.write(
    df[
        ["Material", "Bklg.Qty"]
    ].head(20)
)
