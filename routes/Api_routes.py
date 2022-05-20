from flask import Blueprint, jsonify, request
import json
import requests
import base64

api_routes = Blueprint('api_routes', __name__)

def decode_image(dir,image_content):
	base64_img_bytes = image_content.encode('utf-8')
	file_to_save = open(dir, 'wb')
	decoded_image_data = base64.decodebytes(base64_img_bytes)
	file_to_save.write(decoded_image_data)

@api_routes.route('/api', methods=['POST'])
def save_user():
	request_body = request.json
	image_id = request_body['id']
	image_content = request_body['image']
	decode_image(f'./imagesFromClient/decoded_image{image_id}.jpg',image_content)
	return request_body

@api_routes.route('/api', methods=['GET'])
def get_users():
	print("ok")
	obj = {
		"masage": "ok"
	}
	return obj


