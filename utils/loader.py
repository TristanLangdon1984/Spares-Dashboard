import pan*as as pd
from utils.file_loader im*ort (
    get_latest_backlog,
    *et_latest_mb51
)

def load_backlog*):

    file = get_latest_backlog(*

    return pd.read_excel(
      * file,
        engine="xlrd"
    )*
def load_mb51():

    file = get_*atest_mb51()

    return pd.read_e*cel(
        file,
        engine=*xlrd"
    )
