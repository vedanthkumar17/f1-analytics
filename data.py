import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text

from db import get_database_url


@st.cache_resource(show_spinner=False)
def get_engine():
    return create_engine(get_database_url(), pool_pre_ping=True)


@st.cache_data(ttl=3600, show_spinner=False)
def get_season_races():
    engine = get_engine()
    query = text(
        """
        SELECT circuit_short_name, session_key
        FROM sessions
        WHERE year = :year AND session_name = :session_name
        ORDER BY session_key
        """
    )
    df = pd.read_sql(
        query,
        engine,
        params={"year": 2025, "session_name": "Race"},
    )
    if df.empty:
        return {}
    return dict(zip(df["circuit_short_name"], df["session_key"]))


@st.cache_data(ttl=3600, show_spinner=False)
def get_drivers(session_key):
    engine = get_engine()
    query = text(
        """
        SELECT driver_number, full_name, name_acronym, first_name, last_name, team_name
        FROM drivers
        WHERE session_key = :session_key
        ORDER BY driver_number
        """
    )
    return pd.read_sql(query, engine, params={"session_key": session_key})


@st.cache_data(ttl=3600, show_spinner=False)
def get_laps(session_key):
    engine = get_engine()
    query = text(
        """
        SELECT session_key, driver_number, lap_number,
               duration_sector_1, duration_sector_2, duration_sector_3,
               lap_duration, st_speed, is_pit_out_lap
        FROM laps
        WHERE session_key = :session_key
          AND is_pit_out_lap = FALSE
          AND duration_sector_1 IS NOT NULL
          AND duration_sector_2 IS NOT NULL
          AND duration_sector_3 IS NOT NULL
          AND lap_duration IS NOT NULL
          AND lap_duration < 150
        """
    )
    return pd.read_sql(query, engine, params={"session_key": session_key})


@st.cache_data(ttl=3600, show_spinner=False)
def get_pit_stops(session_key):
    engine = get_engine()
    query = text(
        """
        SELECT session_key, driver_number, lap_number, stop_duration, lane_duration
        FROM pit_stops
        WHERE session_key = :session_key
          AND stop_duration IS NOT NULL
        """
    )
    return pd.read_sql(query, engine, params={"session_key": session_key})
