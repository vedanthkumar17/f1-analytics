import requests
import pandas as pd
import psycopg2

conn = psycopg2.connect(
    dbname="f1_analytics",
    user="postgres",
    password="password123",
    host="localhost"
)
cur = conn.cursor()

# Fetch and load drivers
response1 = requests.get("https://api.openf1.org/v1/drivers?session_key=9693")
df1 = pd.DataFrame(response1.json())

for _, row in df1.iterrows():
    cur.execute("""
        INSERT INTO drivers (driver_number, full_name, team_name, name_acronym, first_name, last_name)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (driver_number) DO NOTHING
    """, (row['driver_number'], row['full_name'], row['team_name'],
          row['name_acronym'], row['first_name'], row['last_name']))

print(f"Drivers loaded: {len(df1)}")

# Fetch and load pit stops
response2 = requests.get("https://api.openf1.org/v1/pit?session_key=9693")
df2 = pd.DataFrame(response2.json())
df2 = df2.dropna(subset=["stop_duration"])

for _, row in df2.iterrows():
    cur.execute("""
        INSERT INTO pit_stops (driver_number, lap_number, stop_duration, lane_duration)
        VALUES (%s, %s, %s, %s)
    """, (row['driver_number'], row['lap_number'],
          row['stop_duration'], row['lane_duration']))

print(f"Pit stops loaded: {len(df2)}")

# Fetch and load laps
response3 = requests.get("https://api.openf1.org/v1/laps?session_key=9693")
df3 = pd.DataFrame(response3.json())
df3 = df3.dropna(subset=["duration_sector_1", "duration_sector_2", "duration_sector_3", "lap_duration"])
df3 = df3[df3["is_pit_out_lap"] == False]

for _, row in df3.iterrows():
    cur.execute("""
        INSERT INTO laps (driver_number, lap_number, duration_sector_1, duration_sector_2, duration_sector_3, lap_duration, st_speed, is_pit_out_lap)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (row['driver_number'], row['lap_number'],
          row['duration_sector_1'], row['duration_sector_2'],
          row['duration_sector_3'], row['lap_duration'],
          row.get('st_speed'), row['is_pit_out_lap']))

print(f"Laps loaded: {len(df3)}")

conn.commit()
cur.close()
conn.close()

print("Pipeline complete.")