import pandas as pd


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_json(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["target_type"] = df["deployable"].apply(classify_target)
    return df


def classify_target(deployable: str) -> str:
    d = deployable.lower()
    if "hab" in d:
        return "HAB"
    if "fobradio" in d or "fob_radio" in d:
        return "RADIO"
    return "OTHER"


def filter_targets(df: pd.DataFrame, targets: list[str]) -> pd.DataFrame:
    return df[df["target_type"].isin(targets)]


def build_player_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    One row per steamID.
    Uses the most recently seen player name as the display name.
    """
    idx = df.groupby("steamID")["timestamp"].idxmax()

    players = (
        df.loc[idx, ["steamID", "playerName"]]
        .rename(columns={"playerName": "display_name"})
        .reset_index(drop=True)
    )

    return players[[
        "display_name",
        "steamID",
    ]]


def damage_by_player(df: pd.DataFrame) -> pd.DataFrame:
    """
    Total damage instances per unique player (steamID).
    """
    return (
        df.groupby("steamID")
        .size()
        .reset_index(name="damage_instances")
        .sort_values("damage_instances", ascending=False)
    )


def damage_by_player_and_target(df: pd.DataFrame) -> pd.DataFrame:
    """
    Damage split by player and target type (HAB vs RADIO).
    """
    return (
        df.groupby(["steamID", "target_type"])
        .size()
        .reset_index(name="damage_instances")
    )
