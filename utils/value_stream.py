import pandas as pd

from utils.loader import load_backlog

from config.excluded_parts import EXCLUDED_PARTS
from config.c4c_parts import C4C_PARTS
from config.obsolete_parts import OBSOLETE_PARTS

try:
    from config.excluded_prefixes import EXCLUDED_PREFIXES
except ImportError:
    EXCLUDED_PREFIXES = []


INSTRUMENT_PARTS = [
    "21.2201",
    "21.2821",
    "45.0001",
    "45.0005",
    "49.0051",
    "49.1501",
    "91.0021"
]


def add_business_days(start_date, business_days):

    if pd.isna(start_date):
        return pd.NaT

    current_date = start_date
    days_added = 0

    while days_added < business_days:

        current_date += pd.Timedelta(days=1)

        if current_date.weekday() < 5:
            days_added += 1

    return current_date


def subtract_business_days(start_date, business_days):

    if pd.isna(start_date):
        return pd.NaT

    current_date = start_date
    days_removed = 0

    while days_removed < business_days:

        current_date -= pd.Timedelta(days=1)

        if current_date.weekday() < 5:
            days_removed += 1

    return current_date


def classify_product(material):

    material = str(material).upper().strip()

    if material.startswith("B"):
        return "TSB"

    if (
        material.startswith("98.")
        or material.startswith("S98.")
        or material.startswith("9800")
        or material.startswith("DS9800")
    ):
        return "DS9800"

    if (
        material.startswith("S091.")
        or material.startswith("91.")
    ):
        return "PRIME"

    if (
        material.startswith("S21.")
        or material.startswith("21.")
        or material.startswith("S49.")
        or material.startswith("49.")
    ):
        return "BOND"

    if (
        material.startswith("S26.")
        or material.startswith("26.")
        or material.startswith("S45.")
        or material.startswith("45.")
    ):
        return "PELORIS"

    if (
        material.startswith("S33.")
        or material.startswith("33.")
    ):
        return "TBE"

    return "OTHER"


def build_filtered_df():

    df = load_backlog()

    df["Material"] = (
        df["Material"]
        .astype(str)
        .str.strip()
    )

    df = df[
        ~df["Material"].isin(EXCLUDED_PARTS)
    ]

    df = df[
        ~df["Material"].isin(C4C_PARTS)
    ]

    for prefix in EXCLUDED_PREFIXES:

        df = df[
            ~df["Material"].str.startswith(prefix)
        ]

    df["Doc. Date"] = pd.to_datetime(
        df["Doc. Date"],
        dayfirst=True,
        errors="coerce"
    )

    df["PD Eff.Dte"] = pd.to_datetime(
        df["PD Eff.Dte"],
        dayfirst=True,
        errors="coerce"
    )

    initial_pack_date = df["Doc. Date"].apply(
        lambda x: add_business_days(x, 3)
    )

    df["Adjusted Target Pack Date"] = initial_pack_date

    date_gap = (
        df["PD Eff.Dte"]
        - initial_pack_date
    ).dt.days

    needs_replan = date_gap > 2

    df.loc[
        needs_replan,
        "Adjusted Target Pack Date"
    ] = df.loc[
        needs_replan,
        "PD Eff.Dte"
    ].apply(
        lambda x: subtract_business_days(x, 3)
    )

    # SAP quantities
    # 1,000 = 1
    # 2,000 = 2
    # 27,000 = 27

    df["Qty"] = pd.to_numeric(
        df["Bklg.Qty"]
        .astype(str)
        .str.replace(",", ".", regex=False),
        errors="coerce"
    ).fillna(0)

    df["StockQty"] = pd.to_numeric(
        df["Stock"]
        .astype(str)
        .str.replace(",", ".", regex=False),
        errors="coerce"
    ).fillna(0)

    df["Product"] = df["Material"].apply(
        classify_product
    )

    df["Status"] = "❌ Short"

    df.loc[
        df["StockQty"] >= df["Qty"],
        "Status"
    ] = "✅ Can Deliver"

    instrument_documents = set(
        df.loc[
            df["Material"].isin(INSTRUMENT_PARTS),
            "Document"
        ]
    )

    df["Instrument"] = (
        df["Document"]
        .isin(instrument_documents)
    )

    obsolete_documents = set(
        df.loc[
            df["Material"].isin(OBSOLETE_PARTS),
            "Document"
        ]
    )

    df["Obsolete"] = (
        df["Document"]
        .isin(obsolete_documents)
    )

print(df[[
    "Material",
    "Bklg.Qty",
    "Stock",
    "Qty",
    "StockQty",
    "Status"
]].head(20))

print(df["Status"].value_counts())

    return df
