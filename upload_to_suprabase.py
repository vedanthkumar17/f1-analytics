import pandas as pd
from sqlalchemy import create_engine
import requests
import psycopg2

DATABASE_URL = "postgresql://postgres:kAEDg3THNot4EKsT@db.dcoegygevtkzbdjhzumn.supabase.co:5432/postgres"

engine = create_engine(DATABASE_URL)

# Drivers
df_drivers = pd.read_csv("drivers.csv")
df_drivers.to_sql("drivers", engine, if_exists="replace", index=False)
print(f"Drivers uploaded: {len(df_drivers)}")

# Pit stops
df_pits = pd.read_csv("pit_stops.csv")
df_pits = df_pits.dropna(subset=["stop_duration"])
df_pits.to_sql("pit_stops", engine, if_exists="replace", index=False)
print(f"Pit stops uploaded: {len(df_pits)}")

# Laps
response = requests.get("https://api.openf1.org/v1/laps?session_key=9693")
df_laps = pd.DataFrame(response.json())
df_laps = df_laps.dropna(subset=["duration_sector_1", "duration_sector_2", "duration_sector_3", "lap_duration"])
df_laps = df_laps[df_laps["is_pit_out_lap"] == False]
df_laps.to_sql("laps", engine, if_exists="replace", index=False)
print(f"Laps uploaded: {len(df_laps)}")

print("All data uploaded to Supabase successfully")