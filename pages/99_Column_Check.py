import streamlit as st
from pathlib import Path

st.write("Current Folder")
st.write(Path.cwd())

st.write("Utils Exists?")
st.write(Path("utils").exists())

if Path("utils").exists():
    st.write(list(Path("utils").glob("*")))
