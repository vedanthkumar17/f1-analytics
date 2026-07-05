import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from data import get_season_races, get_drivers, get_laps, get_pit_stops

st.title("F1 2025 Race Analytics")
st.divider()

season_races = get_season_races()

selected_race = st.selectbox("Select Race", list(season_races.keys()))
session_key = season_races[selected_race]

st.caption(f"Data source: OpenF1 API | {selected_race} | Built by Vedanth Kumar")

df_drivers = get_drivers(session_key)

df_laps_raw = get_laps(session_key)

df_pits_raw = get_pit_stops(session_key)


df_laps_merged = pd.merge(df_laps_raw, df_drivers[["driver_number", "full_name", "team_name"]], on="driver_number")


df_pits_merged = pd.merge(df_pits_raw, df_drivers[["driver_number", "full_name", "team_name"]], on="driver_number")


df_fastest_laps = df_laps_merged.groupby("full_name")["lap_duration"].min().reset_index()
df_fastest_laps.columns = ["driver", "fastest_lap"]
df_fastest_laps = df_fastest_laps.sort_values("fastest_lap").reset_index(drop=True)
df_fastest_laps.index += 1
df_fastest_laps.index.name = "Rank"


fastest_driver = df_fastest_laps.iloc[0]["driver"]
fastest_time = df_fastest_laps.iloc[0]["fastest_lap"]
fastest_pit = df_pits_merged.loc[df_pits_merged["stop_duration"].idxmin()]

col1, col2, col3 = st.columns(3)
col1.metric("Fastest Lap", f"{fastest_driver}")
col2.metric("Fastest Lap Time", f"{fastest_time:.3f}s")
col3.metric("Fastest Pit Stop", f"{fastest_pit['full_name']} - {fastest_pit['stop_duration']}s")


st.subheader("Fastest Lap Times")
st.dataframe(df_fastest_laps, use_container_width=True)

fig = px.bar(df_fastest_laps, x="fastest_lap", y="driver",
             orientation='h',
             title="Fastest Lap Times",
             color="fastest_lap",
             color_continuous_scale="viridis")
fig.update_layout(
    yaxis={'categoryorder':'total ascending'},
    xaxis_range=[df_fastest_laps["fastest_lap"].min() - 1, df_fastest_laps["fastest_lap"].max() + 1]
)
st.plotly_chart(fig, use_container_width=True)


df_pit_avg = df_pits_merged.groupby("full_name")["stop_duration"].mean().round(2).reset_index()
df_pit_avg.columns = ["driver", "avg_stop"]
df_pit_avg = df_pit_avg.sort_values("avg_stop").reset_index(drop=True)
df_pit_avg.index += 1
df_pit_avg.index.name = "Rank"

st.subheader("Pit Stop Performance")
st.dataframe(df_pit_avg, use_container_width=True)

fig = px.bar(df_pit_avg, x="avg_stop", y="driver",
             orientation='h',
             title="Average Pit Stop Duration",
             color="avg_stop",
             color_continuous_scale="viridis")
fig.update_layout(
    yaxis={'categoryorder':'total ascending'},
    xaxis_range=[df_pit_avg["avg_stop"].min() - 0.5, df_pit_avg["avg_stop"].max() + 0.5]
)
st.plotly_chart(fig, use_container_width=True)


df_team_laps = df_laps_merged.groupby("team_name")["lap_duration"].mean().round(2).reset_index()
df_team_laps.columns = ["team", "avg_lap_time"]
df_team_laps = df_team_laps.sort_values("avg_lap_time").reset_index(drop=True)
df_team_laps.index += 1
df_team_laps.index.name = "Rank"

st.subheader("Average Lap Time Per Team")
st.dataframe(df_team_laps, use_container_width=True)

fig = px.bar(df_team_laps, x="avg_lap_time", y="team",
             orientation='h',
             title="Average Lap Time Per Team",
             color="avg_lap_time",
             color_continuous_scale="viridis")
fig.update_layout(
    yaxis={'categoryorder':'total ascending'},
    xaxis_range=[df_team_laps["avg_lap_time"].min() - 1, df_team_laps["avg_lap_time"].max() + 1]
)
st.plotly_chart(fig, use_container_width=True)