#https://stackabuse.com/serving-static-files-with-flask
#https://python-adv-web-apps.readthedocs.io/en/latest/flask3.html
#https://stackoverflow.com/questions/20646822/how-to-serve-static-files-in-flask
#python3 -m http.server 5500 --bind 192.168.1.104

#https://codigofacilito.com/articulos/deploy-flask-heroku

#sudo pip3 install virtualenv
#virtualenv venv
#source venv/bin/activate
#pip3 freeze > requirements.txt
#deactivate

from flask import Flask
from flask_cors import CORS

from routes.User_routes import user_routes

app = Flask(__name__)
CORS(app)

app.register_blueprint(user_routes)

if __name__ == '__main__':
	app.run(debug=True, host="localhost", port=7000)



