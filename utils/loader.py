import pandas as pd

BACKLOG_FILE = "data/ZVREP386 - 3013BACKLOG1.XLS"
MB51_FILE = "data/MB51 - MEL_SPARES.XLS"


def clean_columns(df):

    cols = []

    for col in df.columns:

        col = str(col)

        col = col.replace("\ufeff", "")
        col = col.replace("ÿþ", "")

        col = " ".join(col.split())

        cols.append(col)

    df.columns = cols

    return df


def load_backlog():

    df = pd.read_csv(
        BACKLOG_FILE,
        sep="\t",
        encoding="utf-16-le",
        encoding_errors="ignore",
        engine="python"
    )

    return clean_columns(df)


def load_mb51():

    df = pd.read_csv(
        MB51_FILE,
        sep="\t",
        encoding="utf-16-le",
        encoding_errors="ignore",
        engine="python"
    )

    return clean_columns(df)
