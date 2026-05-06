import requests
import pandas as pd

response = requests.get("https://api.openf1.org/v1/pit?session_key=9158")
data = response.json()

df = pd.DataFrame(data)
print(df.head())

df.to_csv("pit_stops.csv", index=False)
print("Saved to pit_stops.csv")

df_clean = df.dropna(subset=["pit_duration"])
#the above line drops every row where pit_duration is empty.

print(f"Total pit stops: {len(df_clean)}")
print(df_clean[["driver_number", "lap_number", "pit_duration"]])

df_clean.to_csv("pit_stops.csv", index=False)