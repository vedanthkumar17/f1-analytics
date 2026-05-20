import streamlit as st
import psycopg2
import pandas as pd

conn = psycopg2.connect(
    dbname = "f1_analytics",
    user = "postgres",
    password = "password123",
    host = "localhost"
)
st.title("F1 2025 Australian GP Analytics")
st.divider()

st.subheader("Fastest Lap Times")
df_laps = pd.read_sql(""" 
    select d.full_name as Driver, min(l.lap_duration) as fastest_laps from laps l
    join drivers d on l.driver_number = d.driver_number
    group by Driver order by fastest_laps asc;
""", conn)

df_laps = df_laps.reset_index(drop=True)
df_laps.index = df_laps.index + 1
df_laps.index.name = "Rank"

st.dataframe(df_laps, use_container_width=True)

st.subheader("Pit Stop Performance")
df_pits = pd.read_sql("""
    select d.full_name as Driver, round(avg(p.stop_duration)::numeric, 2) as avg_stops
    from pit_stops p
    join drivers d on p.driver_number = d.driver_number
    group by Driver order by avg_stops asc;
""", conn)

df_pits = df_pits.reset_index(drop=True)
df_pits.index = df_pits.index + 1
df_pits.index.name = "Rank"

st.dataframe(df_pits, use_container_width=True)
conn.close()