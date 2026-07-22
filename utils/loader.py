def load_backlog():

    df = pd.read_csv(
        BACKLOG_FILE,
        sep="\t",
        encoding="latin1",
        engine="python"
    )

    df.columns = (
        df.columns
        .str.strip()
        .str.replace("\n", " ", regex=False)
        .str.replace("\r", " ", regex=False)
        .str.replace("  ", " ", regex=False)
    )

    return df
