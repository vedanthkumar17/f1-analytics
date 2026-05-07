import requests
import pandas as pd

response1 = requests.get("https://api.openf1.org/v1/drivers?session_key=9158")
response2 = requests.get("https://api.openf1.org/v1/pit?session_key=9158")

data1 = response1.json()
data2 = response2.json()

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

df_merge = pd.merge(df1, df2, on = "driver_number")
print(f"Total rows: {len(df_merge)}")
df_merge.to_csv("merged.csv", index=False)

df_clean = df_merge.dropna(subset = ["pit_duration"])
print(df_clean.head())
print(f"Real Pit Stops: {len(df_clean)}")
df_clean.to_csv("merged.csv", index=False)