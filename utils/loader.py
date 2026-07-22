import pandas as pd

BACKLOG_FILE = "data/ZVREP386 - 3013BACKLOG1.XLS"
MB51_FILE = "data/MB51 - MEL_SPARES.XLS"


def load_backlog():

    return pd.read_excel(
        BACKLOG_FILE,
        engine="xlrd"
    )


def load_mb51():

    return pd.read_excel(
        MB51_FILE,
        engine="xlrd"
    )
