import pandas as pd

from utils.file_loader import (
    get_latest_backlog,
    get_latest_mb51
)


def load_backlog():

    file = get_latest_backlog()

    return pd.read_excel(
        file,
        sheet_name="ZVREP386 - 3013BACKLOG1",
        engine="openpyxl"
    )


def load_mb51():

    file = get_latest_mb51()

    return pd.read_excel(
        file,
        engine="openpyxl"
    )
