import requests
import pandas

response = requests.get("https://api.openf1.org/v1/sessions?year=2025&session_name=Race")
data = response.json()

sessionKey_dict = {}
df = pandas.DataFrame(data)
sessionKey_dict = dict(zip(df['session_key'], df['country_name']))

df.to_csv("sessions_keys.csv", index = False)
print("Saved to sessions_keys.csv")