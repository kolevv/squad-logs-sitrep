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


def damage_by_player(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("playerName")
        .size()
        .reset_index(name="damage_instances")
        .sort_values("damage_instances", ascending=False)
    )


def damage_by_player_and_target(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["playerName", "target_type"])
        .size()
        .reset_index(name="damage_instances")
        .sort_values("damage_instances", ascending=False)
    )
