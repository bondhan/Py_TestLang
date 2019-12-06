from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config.flask_config_apiserver import app_apiserver

app_isoclient = Flask(__name__)
app_isoclient.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:password@localhost:3306/pylang_db'
app_isoclient.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app_isoclient.config['SQLALCHEMY_POOL_SIZE'] = 1000
app_isoclient.config['SQLALCHEMY_ECHO'] = False
# db_isoclient = SQLAlchemy(app_isoclient)
# db_pylang = SQLAlchemy(app_apiserver)

iso_client_host = "http://127.0.0.1:8080"
iso_client_payment = "/process_payment"