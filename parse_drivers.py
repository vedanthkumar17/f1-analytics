import requests, json

response = requests.get("https://api.openf1.org/v1/drivers?session_key=9693")
data = response.json()
print(json.dumps(data[0], indent=1))
#the above line prints the driver's information.

for driver in data:
    print(f"{driver.get('name_acronym')} - {driver.get('full_name')} - {driver.get('team_name')}")
