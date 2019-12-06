from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

app_apiserver = Flask(__name__)
app_apiserver.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:password@localhost:3306/pylang_db'
app_apiserver.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app_apiserver.config['SQLALCHEMY_POOL_SIZE'] = 1000
app_apiserver.config['SQLALCHEMY_ECHO'] = False


db_pylang = SQLAlchemy(app_apiserver)
ma_apiserver = Marshmallow(app_apiserver)

DEBUG = True