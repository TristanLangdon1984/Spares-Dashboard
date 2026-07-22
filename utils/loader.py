import pandas as pd

BACKLOG_FILE = "data/ZVREP386 - 3013BACKLOG1.XLS"
MB51_FILE = "data/MB51 - MEL_SPARES.XLS"


def clean_columns(df):

    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.replace("\n", " ", regex=False)
        .str.replace("\r", " ", regex=False)
    )

    return df


def load_backlog():

    df = pd.read_csv(
        BACKLOG_FILE,
        sep="\t",
        encoding="latin1",
        engine="python"
    )

    df = clean_columns(df)

    return df


def load_mb51():

    df = pd.read_csv(
        MB51_FILE,
        sep="\t",
        encoding="latin1",
        engine="python"
    )

    df = clean_columns(df)

    return df
