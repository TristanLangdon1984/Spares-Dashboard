from pathlib import Path
*BACKLOG_FOLDER = Path(
    r"C:\Us*rs\ztl\Danaher\LBSM*L Production - Documents\Spares\QD*P data\Daily SAP Backlog Export"
)*
MB51_FOLDER = Path(
    r"C:\User*\ztl\Danaher\LBSMEL Production - D*cuments\Spares\QDIP data\Daily SAP*Productivity Export"
)


def get_l*test_back*og():

    files = list(
        BACKLOG_FOLDER.glob("*.xls*")
    )

    return max(
    *   files,
        key=lambda x: x.*tat().st_mtime
    )


def get_lat*st_mb51():

    files = list(
    *   MB51*FOLDER.glob("*.xls*")
    )

    return max(
        *iles,
        key=lambda x: x.stat*).st_mtime
    )
