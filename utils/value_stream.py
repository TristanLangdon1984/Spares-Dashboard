import pandas as pd


def classify_product(description):

    desc = str(description).upper()

    if "PELORIS" in desc:
        return "PELORIS"

    if "CER" in desc:
        return "CER"

    if "ARC" in desc:
        return "ARC"

    if (
        "BOND" in desc
        or "RX" in desc
        or "PRIME" in desc
        or "BOND-III" in desc
        or "BOND III" in desc
        or "BOND-MAX" in desc
    ):
        return "BOND"

    return "OTHER"
