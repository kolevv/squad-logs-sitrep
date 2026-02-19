import streamlit as st
import plotly.express as px
import pandas as pd

from analysis import (
    load_data,
    build_player_table,
    filter_targets,
    damage_by_player,
    damage_by_player_and_target,
    classify_target,
)

st.set_page_config(page_title="HAB & Radio Damage Analytics",
                   layout="wide")
st.title("HAB & Radio Damage Analytics")

st.sidebar.markdown("Upload a SquadJS JSON log file to continue.")
uploaded_file = st.file_uploader(
    '''Upload JSON file with the following format:

```json
 {
    "messageId": "1234567890123456789",
    "timestamp": "2025-02-13T20:08:07.267Z",
    "playerName": "Bishop",
    "steamID": "01234567890123456",
    "eosID": "0001a2b345c678d90e1fg23456789012",
    "deployable": "US_Hab_Forest",
    "weapon": "BP_PLA_Deployable_TNT_Explosive_Timed"
  },
```''',
    type=["json"],
)
if uploaded_file is None:
    st.stop()
try:
    df = pd.read_json(uploaded_file, dtype={"steamID": str, "eosID": str})
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["target_type"] = df["deployable"].apply(classify_target)
    st.success("Uploaded data loaded successfully.")
except Exception as e:
    st.error(f"Failed to parse uploaded file: {e}")
    st.stop()

players = build_player_table(df)

# Sidebar
st.sidebar.header("Target Selection")
target_mode = st.sidebar.radio(
    "Damage Type",
    options=["HAB only", "Radio only", "HAB + Radio"],
)
target_map = {
    "HAB only": ["HAB"],
    "Radio only": ["RADIO"],
    "HAB + Radio": ["HAB", "RADIO"],
}
filtered_df = filter_targets(df, target_map[target_mode])

# Player filter
player_lookup = dict(zip(players["display_name"], players["steamID"]))
selected_names = st.sidebar.multiselect(
    "Players",
    options=sorted(player_lookup.keys()),
)
if selected_names:
    selected_ids = [player_lookup[n] for n in selected_names]
    filtered_df = filtered_df[filtered_df["steamID"].isin(selected_ids)]

# Top players
st.subheader(f"Top Players — {target_mode}")
by_player = damage_by_player(filtered_df).merge(
    players, on="steamID", how="left")
by_player = by_player[["display_name", "damage_instances", "steamID"]]

fig = px.bar(
    by_player.head(20),
    x="display_name",
    y="damage_instances",
    hover_data={"steamID": True,
                "damage_instances": True, "display_name": False},
    title=f"Top 20 Players ({target_mode})",
)
st.plotly_chart(fig, width='stretch')

st.dataframe(
    by_player,
    width='stretch',
    hide_index=True,
    column_config={
        "steamID": st.column_config.TextColumn("Steam ID"),
        "display_name": st.column_config.TextColumn("Player"),
        "damage_instances": st.column_config.NumberColumn("Damage Instances"),
    },
)

# HAB vs Radio breakdown
st.subheader("HAB vs Radio Breakdown")
breakdown = damage_by_player_and_target(
    df[df["target_type"].isin(["HAB", "RADIO"])]
).merge(players, on="steamID", how="left")

fig2 = px.bar(
    breakdown,
    x="display_name",
    y="damage_instances",
    color="target_type",
    title="HAB vs Radio Damage per Player",
)
st.plotly_chart(fig2, width='stretch')
