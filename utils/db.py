from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
db_uri = 'mysql+pymysql://ull723k51nkuwjps:WJIl1nNcF0gvMvRAQbf5@b84ertg3lptxeayohgqa-mysql.services.clever-cloud.com/b84ertg3lptxeayohgqa'

def database_config(app):
	app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	SQLAlchemy(app)
	Marshmallow(app)