from flask import Blueprint, jsonify, request
import json
import requests

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/api/user', methods=['POST'])
def save_user():
	request_body = request.json
	print(request_body)
	return request_body

@user_routes.route('/api/users', methods=['GET'])
def get_users():
	print("ok")
	return jsonify()


