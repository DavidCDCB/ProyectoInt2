from flask import Blueprint, jsonify, request
import json
import requests

api_routes = Blueprint('api_routes', __name__)

@api_routes.route('/api', methods=['POST'])
def save_user():
	request_body = request.json
	print(request_body)
	return request_body

@api_routes.route('/api', methods=['GET'])
def get_users():
	print("ok")

	obj = {
		"masage": "ok"
	}
	return obj


