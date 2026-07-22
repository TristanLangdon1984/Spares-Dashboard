import streamlit as st

try:
    import utils.file_loader as fl

    st.success("file_loader imported successfully")

    st.write(dir(fl))

except Exception as e:

    st.error(str(e))
