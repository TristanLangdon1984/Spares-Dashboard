import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Data Loads",
    layout="wide"
)

st.title("Data Loads")

# Create data folder if missing
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# --------------------------
# 301 DAILY
# --------------------------

st.subheader("301 Daily")

daily_file = st.file_uploader(
    "Upload 301 Daily File",
    type=["xlsx", "xls", "csv"],
    key="daily"
)

if daily_file:

    try:

        if daily_file.name.lower().endswith(".csv"):

            daily_df = pd.read_csv(daily_file)

        else:

            daily_df = pd.read_excel(
                daily_file
            )

        output_file = (
            data_dir /
            "301daily.xlsx"
        )

        daily_df.to_excel(
            output_file,
            index=False
        )

        c1, c2 = st.columns(2)

        c1.metric(
            "Rows Loaded",
            f"{len(daily_df):,}"
        )

        c2.metric(
            "Columns",
            len(daily_df.columns)
        )

        st.success(
            f"301 Daily saved to {output_file}"
        )

        with st.expander(
            "Preview"
        ):

            st.dataframe(
                daily_df.head(20),
                use_container_width=True
            )

    except Exception as e:

        st.error(
            f"Error loading file: {e}"
        )

# --------------------------
# MB51
# --------------------------

st.divider()

st.subheader("MB51")

mb51_file = st.file_uploader(
    "Upload MB51 File",
    type=["xlsx", "xls", "csv"],
    key="mb51"
)

if mb51_file:

    try:

        if mb51_file.name.lower().endswith(".csv"):

            mb51_df = pd.read_csv(
                mb51_file
            )

        else:

            mb51_df = pd.read_excel(
                mb51_file
            )

        output_file = (
            data_dir /
            "mb51.xlsx"
        )

        mb51_df.to_excel(
            output_file,
            index=False
        )

        c1, c2 = st.columns(2)

        c1.metric(
            "Rows Loaded",
            f"{len(mb51_df):,}"
        )

        c2.metric(
            "Columns",
            len(mb51_df.columns)
        )

        st.success(
            f"MB51 saved to {output_file}"
        )

        with st.expander(
            "Preview"
        ):

            st.dataframe(
                mb51_df.head(20),
                use_container_width=True
            )

    except Exception as e:

        st.error(
            f"Error loading file: {e}"
        )

# --------------------------
# CURRENT FILES
# --------------------------

st.divider()

st.subheader(
    "Current Stored Files"
)

files = []

for file in data_dir.glob("*"):

    files.append(
        {
            "File": file.name,
            "Size KB": round(
                file.stat().st_size / 1024,
                1
            )
        }
    )

if files:

    st.dataframe(
        pd.DataFrame(files),
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No files uploaded yet."
    )
