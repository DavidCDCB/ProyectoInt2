from flask import Blueprint, Response, request
import json
import requests
import base64
import os

api_routes = Blueprint('api_routes', __name__)

def decode_image(dir,image_content):
	base64_img_bytes = image_content.encode('utf-8')
	file_to_save = open(dir, 'wb')
	decoded_image_data = base64.decodebytes(base64_img_bytes)
	file_to_save.write(decoded_image_data)

def create_response(num_images):
	response = {
		"state":"success",
		"results":[
			{
				"model_id":1,
				"results":[]
			}
		]
	}

	for num in range(1, num_images+1):
		# ...
		response["results"][0]["results"].append({
			"class":0,
			"idImagen":num,
		})

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
		response = create_response(len(request_body["images"]))
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


