from pathlib import Path

BACKLOG_FOLDER = Path(
    r"C:\Users\ztl\Danaher\LBSMEL Production - Documents\Spares\QDIP data\Daily SAP Backlog Export"
)

MB51_FOLDER = Path(
    r"C:\Users\ztl\Danaher\LBSMEL Production - Documents\Spares\QDIP data\Daily SAP Productivity Export"
)


def get_latest_backlog():

    backlog_files = list(
        BACKLOG_FOLDER.glob("*.xlsx")
    )

    if not backlog_files:
        raise FileNotFoundError(
            f"No Excel files found in {BACKLOG_FOLDER}"
        )

    return max(
        backlog_files,
        key=lambda x: x.stat().st_mtime
    )


def get_latest_mb51():

    mb51_files = list(
        MB51_FOLDER.glob("*.xlsx")
    )

    if not mb51_files:
        raise FileNotFoundError(
            f"No Excel files found in {MB51_FOLDER}"
        )

    return max(
        mb51_files,
        key=lambda x: x.stat().st_mtime
    )
