import requests
import pandas as pd

response = requests.get("https://api.openf1.org/v1/pit?session_key=9158")
data = response.json()

df = pd.DataFrame(data)
print(df.head())

df.to_csv("pit_stops.csv", index=False)
print("Saved to pit_stops.csv")