import requests, pandas as pd

response = requests.get("https://api.openf1.org/v1/laps?session_key=9693")
data = response.json()

df1 = pd.DataFrame(data)
df2 = pd.read_csv("drivers.csv")
df_merge = pd.merge(df1, df2, on = "driver_number")

df_clean = df_merge.dropna(subset = ["duration_sector_1", 
"duration_sector_2", "duration_sector_3"])

df_clean = df_clean[df_clean["is_pit_out_lap"] == False]

sector1 = df_clean.nsmallest(1, "duration_sector_1")[["full_name", "duration_sector_1"]]
sector2 = df_clean.nsmallest(1, "duration_sector_2")[["full_name", "duration_sector_2"]]
sector3 = df_clean.nsmallest(1, "duration_sector_3")[["full_name", "duration_sector_3"]]

print(f"Fastest in Sector 1:\n {sector1.iloc[0]["full_name"]} and the time taken: {sector1.iloc[0]["duration_sector_1"]}")
print(f"Fastest in Sector 2:\n {sector2.iloc[0]["full_name"]} and the time taken: {sector2.iloc[0]["duration_sector_2"]}")
print(f"Fastest in Sector 3:\n {sector3.iloc[0]["full_name"]} and the time taken: {sector3.iloc[0]["duration_sector_3"]}")
