import argparse
import time

import psycopg2
import requests
from psycopg2.extras import execute_values

from db import get_database_url

BASE_URL = "https://api.openf1.org/v1"
SEASON_YEAR = 2025
REQUEST_TIMEOUT = 30
RATE_LIMIT_SLEEP = 0.5


def fetch_with_retry(url, retries=3, delay=5):
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            data = response.json()
            if isinstance(data, list):
                return data
            print(f"  unexpected response (attempt {attempt + 1}/{retries})")
        except (requests.RequestException, ValueError) as exc:
            print(f"  request failed: {exc} (attempt {attempt + 1}/{retries})")
        if attempt < retries - 1:
            time.sleep(delay)
    return None


def fetch_list(url):
    data = fetch_with_retry(url)
    if data is None:
        print(f"  WARNING: no data returned from {url}; treating as empty")
    return data or []


def to_int(value):
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def to_float(value):
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def upsert_sessions(cur, sessions):
    rows = [
        (
            to_int(s.get("session_key")),
            s.get("circuit_short_name"),
            s.get("country_name"),
            s.get("session_name"),
            to_int(s.get("year")),
        )
        for s in sessions
    ]
    rows = [r for r in rows if r[0] is not None]
    if not rows:
        return 0
    execute_values(
        cur,
        """
        INSERT INTO sessions (session_key, circuit_short_name, country_name, session_name, year)
        VALUES %s
        ON CONFLICT (session_key) DO UPDATE SET
            circuit_short_name = EXCLUDED.circuit_short_name,
            country_name = EXCLUDED.country_name,
            session_name = EXCLUDED.session_name,
            year = EXCLUDED.year
        """,
        rows,
    )
    return len(rows)


def upsert_drivers(cur, session_key, drivers):
    rows = [
        (
            session_key,
            to_int(d.get("driver_number")),
            d.get("full_name"),
            d.get("name_acronym"),
            d.get("first_name"),
            d.get("last_name"),
            d.get("team_name"),
        )
        for d in drivers
    ]
    rows = [r for r in rows if r[1] is not None]
    if not rows:
        return 0
    execute_values(
        cur,
        """
        INSERT INTO drivers (session_key, driver_number, full_name, name_acronym, first_name, last_name, team_name)
        VALUES %s
        ON CONFLICT (session_key, driver_number) DO UPDATE SET
            full_name = EXCLUDED.full_name,
            name_acronym = EXCLUDED.name_acronym,
            first_name = EXCLUDED.first_name,
            last_name = EXCLUDED.last_name,
            team_name = EXCLUDED.team_name
        """,
        rows,
    )
    return len(rows)


def upsert_laps(cur, session_key, laps, known_drivers):
    deduped = {}
    skipped_no_lap = 0
    skipped_unknown_driver = 0
    for lap in laps:
        driver_number = to_int(lap.get("driver_number"))
        lap_number = to_int(lap.get("lap_number"))
        if lap_number is None:
            skipped_no_lap += 1
            continue
        if driver_number not in known_drivers:
            skipped_unknown_driver += 1
            continue
        is_pit_out = lap.get("is_pit_out_lap")
        deduped[(driver_number, lap_number)] = (
            session_key,
            driver_number,
            lap_number,
            to_float(lap.get("duration_sector_1")),
            to_float(lap.get("duration_sector_2")),
            to_float(lap.get("duration_sector_3")),
            to_float(lap.get("lap_duration")),
            to_float(lap.get("st_speed")),
            bool(is_pit_out) if is_pit_out is not None else False,
        )
    rows = list(deduped.values())
    if rows:
        execute_values(
            cur,
            """
            INSERT INTO laps (
                session_key, driver_number, lap_number,
                duration_sector_1, duration_sector_2, duration_sector_3,
                lap_duration, st_speed, is_pit_out_lap
            )
            VALUES %s
            ON CONFLICT (session_key, driver_number, lap_number) DO UPDATE SET
                duration_sector_1 = EXCLUDED.duration_sector_1,
                duration_sector_2 = EXCLUDED.duration_sector_2,
                duration_sector_3 = EXCLUDED.duration_sector_3,
                lap_duration = EXCLUDED.lap_duration,
                st_speed = EXCLUDED.st_speed,
                is_pit_out_lap = EXCLUDED.is_pit_out_lap
            """,
            rows,
        )
    return len(rows), skipped_no_lap, skipped_unknown_driver


def upsert_pit_stops(cur, session_key, pit_stops, known_drivers):
    deduped = {}
    skipped_no_lap = 0
    skipped_unknown_driver = 0
    for pit in pit_stops:
        driver_number = to_int(pit.get("driver_number"))
        lap_number = to_int(pit.get("lap_number"))
        if lap_number is None:
            skipped_no_lap += 1
            continue
        if driver_number not in known_drivers:
            skipped_unknown_driver += 1
            continue
        deduped[(driver_number, lap_number)] = (
            session_key,
            driver_number,
            lap_number,
            to_float(pit.get("stop_duration") or pit.get("pit_duration")),
            to_float(pit.get("lane_duration")),
        )
    rows = list(deduped.values())
    if rows:
        execute_values(
            cur,
            """
            INSERT INTO pit_stops (session_key, driver_number, lap_number, stop_duration, lane_duration)
            VALUES %s
            ON CONFLICT (session_key, driver_number, lap_number) DO UPDATE SET
                stop_duration = EXCLUDED.stop_duration,
                lane_duration = EXCLUDED.lane_duration
            """,
            rows,
        )
    return len(rows), skipped_no_lap, skipped_unknown_driver


def main():
    parser = argparse.ArgumentParser(
        description=f"Ingest {SEASON_YEAR} F1 Race data from OpenF1 into PostgreSQL."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Only load the first N sessions.",
    )
    args = parser.parse_args()

    conn = psycopg2.connect(get_database_url())
    conn.autocommit = False
    cur = conn.cursor()

    print(f"Fetching {SEASON_YEAR} Race sessions...")
    sessions = fetch_list(f"{BASE_URL}/sessions?year={SEASON_YEAR}&session_name=Race")
    if not sessions:
        print("No sessions returned. Aborting.")
        cur.close()
        conn.close()
        return

    loaded = upsert_sessions(cur, sessions)
    conn.commit()
    print(f"Sessions upserted: {loaded}")
    time.sleep(RATE_LIMIT_SLEEP)

    session_keys = sorted(
        {to_int(s.get("session_key")) for s in sessions if to_int(s.get("session_key")) is not None}
    )
    if args.limit is not None:
        session_keys = session_keys[: args.limit]
        print(f"Limiting to first {len(session_keys)} sessions.")

    for session_key in session_keys:
        try:
            print(f"\nSession {session_key}: fetching drivers...")
            drivers = fetch_list(f"{BASE_URL}/drivers?session_key={session_key}")
            time.sleep(RATE_LIMIT_SLEEP)
            n_drivers = upsert_drivers(cur, session_key, drivers)
            known_drivers = {
                to_int(d.get("driver_number"))
                for d in drivers
                if to_int(d.get("driver_number")) is not None
            }
            conn.commit()
            print(f"  drivers upserted: {n_drivers}")

            print(f"Session {session_key}: fetching laps...")
            laps = fetch_list(f"{BASE_URL}/laps?session_key={session_key}")
            time.sleep(RATE_LIMIT_SLEEP)
            n_laps, skip_lap_no_lap, skip_lap_unknown = upsert_laps(
                cur, session_key, laps, known_drivers
            )
            conn.commit()
            print(
                f"  laps upserted: {n_laps} "
                f"(skipped {skip_lap_no_lap} missing lap_number, "
                f"{skip_lap_unknown} unknown driver)"
            )

            print(f"Session {session_key}: fetching pit stops...")
            pit_stops = fetch_list(f"{BASE_URL}/pit?session_key={session_key}")
            time.sleep(RATE_LIMIT_SLEEP)
            n_pits, skip_pit_no_lap, skip_pit_unknown = upsert_pit_stops(
                cur, session_key, pit_stops, known_drivers
            )
            conn.commit()
            print(
                f"  pit stops upserted: {n_pits} "
                f"(skipped {skip_pit_no_lap} missing lap_number, "
                f"{skip_pit_unknown} unknown driver)"
            )
        except Exception as exc:
            conn.rollback()
            print(f"ERROR: session {session_key} failed: {exc}; rolling back and continuing")
            continue

    cur.close()
    conn.close()
    print("\nIngestion complete.")


if __name__ == "__main__":
    main()
