import streamlit as st
import plotly.express as px

from analysis import (
    load_data,
    filter_targets,
    damage_by_player,
    damage_by_player_and_target,
)

st.set_page_config(page_title="HAB & Radio Damage Analytics", layout="wide")
st.title("💥 HAB & Radio Damage Analytics")

df = load_data("data/output.json")

# --- Sidebar ---
st.sidebar.header("Target Selection")

target_mode = st.sidebar.radio(
    "Damage Type",
    options=[
        "HAB only",
        "Radio only",
        "HAB + Radio",
    ],
)

target_map = {
    "HAB only": ["HAB"],
    "Radio only": ["RADIO"],
    "HAB + Radio": ["HAB", "RADIO"],
}

filtered_df = filter_targets(df, target_map[target_mode])

# Optional filters
players = st.sidebar.multiselect(
    "Players",
    options=sorted(filtered_df["playerName"].unique()),
)

if players:
    filtered_df = filtered_df[filtered_df["playerName"].isin(players)]

# --- Top offenders ---
st.subheader(f"🔥 Top Players – {target_mode}")

by_player = damage_by_player(filtered_df)

fig = px.bar(
    by_player.head(20),
    x="playerName",
    y="damage_instances",
    title=f"Top 20 Players ({target_mode})",
)

st.plotly_chart(fig, width='stretch')
st.dataframe(by_player, width='stretch')

# --- Breakdown view ---
st.subheader("📊 Player Breakdown (HAB vs Radio)")

breakdown = damage_by_player_and_target(
    df[df["target_type"].isin(["HAB", "RADIO"])]
)

fig2 = px.bar(
    breakdown,
    x="playerName",
    y="damage_instances",
    color="target_type",
    title="HAB vs Radio Damage by Player",
)

st.plotly_chart(fig2, width='stretch')
