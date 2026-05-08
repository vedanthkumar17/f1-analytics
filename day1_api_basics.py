import requests
import json

response = requests.get("https://api.openf1.org/v1/drivers?session_key=9693")

data = response.json()

print(json.dumps(data, indent=2))

#JSON is just a text file 
#that stores data in a structured way that both humans and 
#computers can read easily.

"""
The reason it exists is because when two computers talk to each other over 
the internet they need to agree on a format. 
JSON is that agreed format. 
Every programming language in the world — Python, JavaScript, Java, 
whatever — can read JSON. That's why it became the standard for APIs.
"""