import pandas as pd
import requests
import streamlit as st

@st.cache_data(ttl=3600, show_spinner=False)
def get_season_races():
    response = requests.get("https://api.openf1.org/v1/sessions?year=2025&session_name=Race")
    df = pd.DataFrame(response.json())
    return dict(zip(df['circuit_short_name'], df['session_key']))

@st.cache_data(ttl=3600, show_spinner=False)
def get_drivers(session_key):
    response = requests.get(f"https://api.openf1.org/v1/drivers?session_key={session_key}")
    data = response.json()
    print(type(data))
    print(data)
    print(type(data), data)
    return pd.DataFrame(data)

@st.cache_data(ttl=3600, show_spinner=False)
def get_laps(session_key):
    response = requests.get(f"https://api.openf1.org/v1/laps?session_key={session_key}")
    df = pd.DataFrame(response.json())
    df = df.dropna(subset=["duration_sector_1", "duration_sector_2", "duration_sector_3", "lap_duration"])
    df = df[df["is_pit_out_lap"] == False]
    df = df[df["lap_duration"] < 150]
    return df

@st.cache_data(ttl=3600, show_spinner=False)
def get_pit_stops(session_key):
    response = requests.get(f"https://api.openf1.org/v1/pit?session_key={session_key}")
    df = pd.DataFrame(response.json())
    df = df.dropna(subset=["stop_duration"])
    return df