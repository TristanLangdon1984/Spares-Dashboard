import pandas as pd

BACKLOG_FILE = "data/ZVREP386 - 3013BACKLOG1.XLS"
MB51_FILE = "data/MB51 - MEL_SPARES.XLS"


def load_backlog():

    return pd.read_csv(
        BACKLOG_FILE,
        sep="\t",
        encoding="utf-16",
        encoding_errors="ignore",
        engine="python"
    )


def load_mb51():

    return pd.read_csv(
        MB51_FILE,
        sep="\t",
        encoding="utf-16",
        encoding_errors="ignore",
        engine="python"
    )
