import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

import plotly.express as px

DATABASE_URL = st.secrets["DATABASE_URL"]
engine = create_engine(DATABASE_URL)

st.title("F1 2025 Australian GP Analytics")
st.caption("📍 Albert Park Grand Prix Circuit, Melbourne | March 14-16, 2025")

st.divider()
st.caption("Data source: OpenF1 API | 2025 Australian GP | Built by Vedanth Kumar")

st.metric("Fastest Lap", "Lando Norris - 82.167s")
st.metric("Fastest Pit Stop", "Charles Leclerc - 2.3s")
st.metric("Total Pit Stops Analyzed", "34")

st.subheader("Fastest Lap Times")
df_laps = pd.read_sql(""" 
    select d.full_name as Driver, min(l.lap_duration) as fastest_laps from laps l
    join drivers d on l.driver_number = d.driver_number
    group by d.full_name order by fastest_laps asc;
""", engine)

df_laps = df_laps.reset_index(drop=True)
df_laps.index = df_laps.index + 1
df_laps.index.name = "Rank"

st.subheader("Lap Stop Performance - Visual")
st.dataframe(df_laps, use_container_width=True)

fig = px.bar(df_laps, x="fastest_laps", y="driver",
             orientation='h',
             title="Fastest Lap Times",
             color="fastest_laps",
             color_continuous_scale="icefire")
fig.update_layout(
    yaxis={'categoryorder':'total ascending'},
    xaxis_range=[81, df_laps['fastest_laps'].max() + 1]
)
st.plotly_chart(fig, use_container_width=True)


st.subheader("Pit Stop Performance")
df_pits = pd.read_sql("""
    select d.full_name as driver, round(avg(p.stop_duration)::numeric, 2) as avg_stops
    from pit_stops p
    join drivers d on p.driver_number = d.driver_number
    group by d.full_name order by avg_stops asc;
""", engine)

df_pits = df_pits.reset_index(drop=True)
df_pits.index = df_pits.index + 1
df_pits.index.name = "Rank"

st.subheader("Pit Stop Performance - Visual")

st.dataframe(df_pits, use_container_width=True)
fig = px.bar(df_pits, x="avg_stops", y="driver",
             orientation='h',
             title="Pit Stop Performance",
             color="avg_stops",
             color_continuous_scale="icefire")
fig.update_layout(
    yaxis={'categoryorder':'total ascending'},
    xaxis_range=[2, df_pits['avg_stops'].max() + 0.5]
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Average Lap Time Per Team")
df_avgLapTime = pd.read_sql("""
    select d.team_name, round(avg(l.lap_duration)::numeric, 2) as avg_lap_time from drivers d
    join laps l on d.driver_number = l.driver_number WHERE l.lap_duration < 150
    group by d.team_name order by avg(l.lap_duration) asc;
""", engine)

df_avgLapTime = df_avgLapTime.reset_index(drop=True)
df_avgLapTime.index = df_avgLapTime.index + 1
df_avgLapTime.index.name = "Rank"

st.subheader("Average Lap Time Per Team - Visual")

st.dataframe(df_avgLapTime, use_container_width=True)

fig = px.bar(df_avgLapTime, x="avg_lap_time", y="team_name",
             orientation='h',
             title="Average Lap Time Per Team",
             color="avg_lap_time",
             color_continuous_scale="icefire")
fig.update_layout(
    yaxis={'categoryorder':'total ascending'},
    xaxis_range=[81, df_avgLapTime['avg_lap_time'].max() + 1]
)
st.plotly_chart(fig, use_container_width=True)