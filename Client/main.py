import requests
import base64
import json

URL_API = "http://localhost:7000/api"

def encode_image(dir)->str:
    binary_file = open(dir, 'rb')
    binary_file_data = binary_file.read()
    base64_encoded_data = base64.b64encode(binary_file_data)
    base64_message = base64_encoded_data.decode('utf-8')
    return base64_message


obj_image = {
    "id":1,
    "image": encode_image('./images/recorte1.jpg')
}

data  = requests.post(URL_API, json=obj_image)
print(data.json())


data = requests.get(URL_API)
print(data.json())