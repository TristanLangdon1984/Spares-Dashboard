import pandas as pd

BACKLOG_FILE = "data/ZVREP386 - 3013BACKLOG1.XLS"
MB51_FILE = "data/MB51 - MEL_SPARES.XLS"


def clean_columns(df):

    df.columns = (
        df.columns.astype(str)
        .str.replace("\ufeff", "", regex=False)
        .str.strip()
    )

    return df


def load_backlog():

    df = pd.read_csv(
        BACKLOG_FILE,
        sep="\t",
        encoding="utf-16-le",
        encoding_errors="ignore",
        engine="python"
    )

    df = clean_columns(df)

    keep_columns = [
        "Doc. Date",
        "RSD",
        "PD Eff.Dte",
        "Document",
        "Material",
        "Material Description",
        "Bklg.Qty",
        "Stock",
        "ShipToCtry",
        "Plnt",
        "Express De"
        "DL"
    ]

    existing_columns = [
        col
        for col in keep_columns
        if col in df.columns
    ]

    return df[existing_columns]


def load_mb51():

    df = pd.read_csv(
        MB51_FILE,
        sep="\t",
        encoding="utf-16-le",
        encoding_errors="ignore",
        engine="python"
    )

    return clean_columns(df)


# Compatibility function

def load_metrics():

    return load_backlog()
