import pandas as pd
import requests
import streamlit as st
import time

def fetch_with_retry(url, retries=3, delay=5):
    for i in range(retries):
        response = requests.get(url)
        data = response.json()
        if isinstance(data, list):
            return data
        time.sleep(delay)
    return None

@st.cache_data(ttl=3600, show_spinner=False)
def get_season_races():
    data = fetch_with_retry("https://api.openf1.org/v1/sessions?year=2025&session_name=Race")
    if data is None:
        return {}
    df = pd.DataFrame(data)
    return dict(zip(df['circuit_short_name'], df['session_key']))

@st.cache_data(ttl=3600, show_spinner=False)
def get_drivers(session_key):
    data = fetch_with_retry(f"https://api.openf1.org/v1/drivers?session_key={session_key}")
    if data is None:
        return pd.DataFrame()
    return pd.DataFrame(data)

@st.cache_data(ttl=3600, show_spinner=False)
def get_laps(session_key):
    data = fetch_with_retry(f"https://api.openf1.org/v1/laps?session_key={session_key}")
    if data is None:
        return pd.DataFrame()
    df = pd.DataFrame(data)
    df = df.dropna(subset=["duration_sector_1", "duration_sector_2", "duration_sector_3", "lap_duration"])
    df = df[df["is_pit_out_lap"] == False]
    df = df[df["lap_duration"] < 150]
    return df

@st.cache_data(ttl=3600, show_spinner=False)
def get_pit_stops(session_key):
    data = fetch_with_retry(f"https://api.openf1.org/v1/pit?session_key={session_key}")
    if data is None:
        return pd.DataFrame()
    df = pd.DataFrame(data)
    return df.dropna(subset=["stop_duration"])