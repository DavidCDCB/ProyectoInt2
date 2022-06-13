from flask import Blueprint, Response, request
import json
import requests
import base64
import os
import time

from Prediccion import  Prediccion as Predict

api_routes = Blueprint('api_routes', __name__)

def decode_image(dir,image_content):
	base64_img_bytes = image_content.encode('utf-8')
	file_to_save = open(dir, 'wb')
	decoded_image_data = base64.decodebytes(base64_img_bytes)
	file_to_save.write(decoded_image_data)

def create_response(models,num_images):
	response = {
		"state":"success",
		"results":[]
	}

	for m in models:
		response["results"].append({
			"model_id":m,
			"results":[]
		})
		inicio = time.time()
		modelo = Predict(f"./ModelFactory/models/modelo{m}.h5",256,256)
		
		for j in range(1, num_images+1):
			# ...
			
			categoria = modelo.predecir(f"./imagesFromClient/decoded_image{j}.jpg")
			
			response["results"][models.index(m)]["results"].append({
				"class":categoria,
				"idImagen":j,
			})
		fin = time.time()
		print(f"tiempo de respuesta para{m}: "+str(fin-inicio))

	return response

@api_routes.route('/api', methods=['POST'])
def save_user():
	# Recorre la carpeta de imagenes para eliminar lo anterior
	test = os.listdir("./imagesFromClient/")
	for item in test:
		if item.endswith(".jpg"):
			os.remove(os.path.join("./imagesFromClient/", item))

	request_body = request.json
	for key in request_body["images"]:
		print(key['id'])
		image_id = key['id']
		image_content = key['image']
		decode_image(f'./imagesFromClient/decoded_image{image_id}.jpg',image_content)

	try:
		print(request_body["models"])
		response = create_response(request_body["models"],len(request_body["images"]))
		return Response(json.dumps(response),status=200,mimetype='application/json')
	except Exception as e:
		return Response(
			json.dumps({
				"state":"error",
				"message":str(e)
			}),
			status=400,
			mimetype='application/json'
		)

@api_routes.route('/api', methods=['GET'])
def get_users():
	print("ok")
	obj = {
		"masage": "ok"
	}
	return obj


