from pathlib import Path

BACKLOG_FOLDER = Path(
    r"C:\Users\ztl\Danaher\LBSMEL Production - Documents\Spares\QDIP data\Daily SAP Backlog Export"
)

MB51_FOLDER = Path(
    r"C:\Users\ztl\Danaher\LBSMEL Production - Documents\Spares\QDIP data\Daily SAP Productivity Export"
)


def get_latest_backlog():

    files = list(
        BACKLOG_FOLDER.glob("*.xls*")
    )

    if len(files) == 0:
        raise FileNotFoundError(
            f"No Excel files found in {BACKLOG_FOLDER}"
        )

    return max(
        files,
        key=lambda x: x.stat().st_mtime
    )


def get_latest_mb51():

    files = list(
        MB51_FOLDER.glob("*.xls*")
    )

    if len(files) == 0:
        raise FileNotFoundError(
            f"No Excel files found in {MB51_FOLDER}"
        )

    return max(
        files,
        key=lambda x: x.stat().st_mtime
    )
