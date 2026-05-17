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

response = requests.get("https://api.openf1.org/v1/laps?session_key=9693")
data = response.json()
df = pd.DataFrame(data)

df = df.dropna(subset=["duration_sector_1", "duration_sector_2", "duration_sector_3", "lap_duration"])
df = df[df["is_pit_out_lap"] == False]

print(f"Loading {len(df)} laps")

for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO laps (driver_number, lap_number, duration_sector_1, duration_sector_2, duration_sector_3, lap_duration, st_speed, is_pit_out_lap)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (row['driver_number'], row['lap_number'],
          row['duration_sector_1'], row['duration_sector_2'],
          row['duration_sector_3'], row['lap_duration'],
          row.get('st_speed'), row['is_pit_out_lap']))

conn.commit()
cur.close()
conn.close()
print("Laps loaded successfully")