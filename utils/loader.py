import pandas as pd

BACKLOG_FILE = "data/ZVREP386 - 3013BACKLOG1.XLS"
MB51_FILE = "data/MB51 - MEL_SPARES.XLS"


def load_backlog():

    df = pd.read_csv(
        BACKLOG_FILE,
        sep="\t",
        encoding="latin1",
        engine="python"
    )

    df.columns = df.columns.str.strip()

    return df


def load_mb51():

    df = pd.read_csv(
        MB51_FILE,
        sep="\t",
        encoding="latin1",
        engine="python"
    )

    df.columns = df.columns.str.strip()

    return df
