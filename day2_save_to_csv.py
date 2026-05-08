import requests
import pandas

response = requests.get("https://api.openf1.org/v1/drivers?session_key=9693")
data = response.json()

df = pandas.DataFrame(data)
print(df.head())

df.to_csv("drivers.csv", index = False)
print("Saved to drivers.csv")