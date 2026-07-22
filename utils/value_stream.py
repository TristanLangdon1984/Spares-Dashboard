def classify_value_stream(desc):

    desc = str(desc).upper()

    if "PELORIS" in desc:
        return "PELORIS"

    if "CER" in desc:
        return "CER"

    if "ARC" in desc:
        return "ARC"

    if (
        "BOND" in desc
        or "BOND-III" in desc
        or "BOND-PRIME" in desc
        or "BOND RX" in desc
        or "BOND-MAX" in desc
    ):
        return "BOND"

    return "OTHER"
