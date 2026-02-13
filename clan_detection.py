import re
import pandas as pd
from itertools import combinations

TAG_REGEX = re.compile(r"[\[\(=|].+?[\]\)=|]")


def extract_tag(name: str):
    m = TAG_REGEX.search(name)
    return m.group(0) if m else None


def detect_name_tag_groups(df: pd.DataFrame):
    df["tag"] = df["playerName"].apply(extract_tag)
    return (
        df.dropna(subset=["tag"])
          .groupby("tag")["playerName"]
          .unique()
          .reset_index()
    )
