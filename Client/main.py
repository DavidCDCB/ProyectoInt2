import requests
import json

data = requests.get("http://localhost:7000/api")
print(data.json())

data  = requests.post("http://localhost:7000/api", json={"name": "juan", "lastname": "perez"})
print(data.json())
