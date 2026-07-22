import pandas as pd

BACKLOG_FILE = "data/ZVREP386 - 3013BACKLOG1.XLS"
MB51_FILE = "data/MB51 - MEL_SPARES.XLS"


def load_backlog():

    try:
        return pd.read_excel(
            BACKLOG_FILE,
            engine="xlrd"
        )
    except Exception:
        tables = pd.read_html(BACKLOG_FILE)
        return tables[0]


def load_mb51():

    try:
        return pd.read_excel(
            MB51_FILE,
            engine="xlrd"
        )
    except Exception:
        tables = pd.read_html(MB51_FILE)
        return tables[0]
``
