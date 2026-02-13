import streamlit as st
import plotly.express as px

from analysis import (
    load_data,
    build_player_table,
    filter_targets,
    damage_by_player,
    damage_by_player_and_target,
)

# ---------- App setup ----------

st.set_page_config(
    page_title="HAB & Radio Damage Analytics",
    layout="wide",
)

st.title("💥 HAB & Radio Damage Analytics")


# ---------- Load data ----------

df = load_data("data/output.json")
players = build_player_table(df)


# ---------- Sidebar ----------

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


# Player filter (name → steamID)
player_lookup = dict(
    zip(players["display_name"], players["steamID"])
)

selected_names = st.sidebar.multiselect(
    "Players",
    options=sorted(player_lookup.keys()),
)

if selected_names:
    selected_ids = [player_lookup[n] for n in selected_names]
    filtered_df = filtered_df[filtered_df["steamID"].isin(selected_ids)]


# ---------- Top players ----------

st.subheader(f"🔥 Top Players — {target_mode}")

by_player = damage_by_player(filtered_df)

# Join display names
by_player = by_player.merge(players, on="steamID", how="left")

# Canonical display order
by_player = by_player[[
    "display_name",
    "damage_instances",
    "steamID",
]]

fig = px.bar(
    by_player.head(20),
    x="display_name",
    y="damage_instances",
    hover_data={
        "steamID": True,
        "damage_instances": True,
        "display_name": False,
    },
    title=f"Top 20 Players ({target_mode})",
)

st.plotly_chart(fig, width='stretch')
st.dataframe(by_player, width='stretch', hide_index=True)


# ---------- HAB vs Radio breakdown ----------

st.subheader("📊 HAB vs Radio Breakdown")

breakdown = damage_by_player_and_target(
    df[df["target_type"].isin(["HAB", "RADIO"])]
)

breakdown = breakdown.merge(players, on="steamID", how="left")

fig2 = px.bar(
    breakdown,
    x="display_name",
    y="damage_instances",
    color="target_type",
    title="HAB vs Radio Damage per Player",
)

st.plotly_chart(fig2, width='stretch')
