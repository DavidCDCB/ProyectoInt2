from logging import captureWarnings
import requests
import base64
import json

URL_API = "http://localhost:7000/api"

#Método para codificar imágen en base 64
def encode_image(dir)->str:
    binary_file = open(dir, 'rb')
    binary_file_data = binary_file.read()
    base64_encoded_data = base64.b64encode(binary_file_data)
    base64_message = base64_encoded_data.decode('utf-8')
    return base64_message


#1. Se guarda cada imagen en una lista y se codifica
#2. Luego se convierten la lista a json
#3. Se envía la petición al servidor
def codificarEnviar(number_image):
    imagenes = []
    request_object = {
        "id_client":1,
        "models":[]
    }
    
    for n in range(1, number_image):
        obj_image = {
            "id":n,
            "image": encode_image("./images/recorte{}.jpg".format(n))
            #"image": "imagen simulada{}".format(n)
        }
        imagenes.append(obj_image)

    request_object["images"] = imagenes
    data  = requests.post(URL_API, json=request_object)
    print(json.dumps(data.json(), indent=4, sort_keys=True))
