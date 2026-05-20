import pandas as pd
import psycopg2

conn = psycopg2.connect(
    dbname="f1_analytics",
    user="postgres",
    password="password123",
    host="localhost"
)

cur = conn.cursor()

df_drivers = pd.read_csv("drivers.csv")

for _, row in df_drivers.iterrows():
    cur.execute("""
        INSERT INTO drivers (driver_number, full_name, team_name, name_acronym, first_name, last_name)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (driver_number) DO NOTHING
    """, (row['driver_number'], row['full_name'], row['team_name'], 
          row['name_acronym'], row['first_name'], row['last_name']))

df_pits = pd.read_csv("pit_stops.csv")
df_pits = df_pits.dropna(subset=["stop_duration"])
print(f"Loading {len(df_pits)} pit stops with valid stop duration")
for _, row in df_pits.iterrows():
    cur.execute("""
        INSERT INTO pit_stops (driver_number, lap_number, stop_duration, lane_duration)
        VALUES (%s, %s, %s, %s)
    """, (row['driver_number'], row['lap_number'], 
          row.get('stop_duration'), row['lane_duration']))

conn.commit()
cur.close()
conn.close()

print("Data loaded successfully")

# The ON CONFLICT clause in the drivers insertion ensures that if a driver with the same driver_number already exists, 
# it will skip inserting that record, preventing duplicates.