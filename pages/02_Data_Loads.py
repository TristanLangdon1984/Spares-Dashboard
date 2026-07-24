import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Data Loads",
    layout="wide"
)

st.title("Data Loads")

data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# --------------------------
# 301 DAILY
# --------------------------

st.subheader("301 Daily")

daily_file = st.file_uploader(
    "Upload 301 Daily File",
    type=["xls", "xlsx", "csv"],
    key="daily"
)

if daily_file is not None:

    try:

        output_file = (
            data_dir /
            "ZVREP386 - 3013BACKLOG1.XLS"
        )

        with open(
            output_file,
            "wb"
        ) as f:

            f.write(
                daily_file.getbuffer()
            )
st.success("301 Daily uploaded successfully")

st.write("Saved to:")
st.code(str(output_file.resolve()))

st.write("File exists:")
st.write(output_file.exists())

st.write("Size on disk:")
st.write(output_file.stat().st_size)

    except Exception as e:

        st.error(
            f"Error saving file: {e}"
        )

# --------------------------
# MB51
# --------------------------

st.divider()

st.subheader("MB51")

mb51_file = st.file_uploader(
    "Upload MB51 File",
    type=["xls", "xlsx", "csv"],
    key="mb51"
)

if mb51_file is not None:

    try:

        output_file = (
            data_dir /
            "MB51 - MEL_SPARES.XLS"
        )

        with open(
            output_file,
            "wb"
        ) as f:

            f.write(
                mb51_file.getbuffer()
            )

        st.success(
            f"""
MB51 uploaded successfully

File: {output_file.name}

Uploaded: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')}
"""
        )

        st.metric(
            "File Size KB",
            round(
                len(
                    mb51_file.getbuffer()
                ) / 1024,
                1
            )
        )

    except Exception as e:

        st.error(
            f"Error saving file: {e}"
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

    modified = pd.Timestamp(
        file.stat().st_mtime,
        unit="s"
    )

    files.append(
        {
            "File": file.name,
            "Last Updated": modified.strftime(
                "%d/%m/%Y %H:%M:%S"
            ),
            "Size KB": round(
                file.stat().st_size / 1024,
                1
            )
        }
    )

if files:

    files_df = pd.DataFrame(files)

    files_df = files_df.sort_values(
        by="Last Updated",
        ascending=False
    )

    st.dataframe(
        files_df,
        width="stretch",
        hide_index=True
    )

else:

    st.info(
        "No files uploaded yet."
    )
