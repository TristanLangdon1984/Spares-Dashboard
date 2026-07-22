import pandas as pd

BACKLOG_FILE = "data/ZVREP386 - 3013BACKLOG1.XLS"
MB51_FILE = "data/MB51 - MEL_SPARES.XLS"


def clean_columns(df):

    cols = []

    for col in df.columns:

        col = str(col)

        col = col.replace("\ufeff", "")
        col = col.replace("ÿþ", "")
        col = col.strip()

        cols.append(col)

    df.columns = cols

    return df


def read_sap_file(filename):

    try:

        df = pd.read_csv(
            filename,
            sep="\t",
            encoding="utf-16-le",
            encoding_errors="ignore",
            engine="python"
        )

        return clean_columns(df)

    except Exception:

        df = pd.read_csv(
            filename,
            sep="\t",
            encoding="latin1",
            engine="python"
        )

        return clean_columns(df)


def load_backlog():

    return read_sap_file(BACKLOG_FILE)


def load_mb51():

    return read_sap_file(MB51_FILE)
