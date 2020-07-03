from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config
import api.ebe.lib as ebe

api = Flask(__name__)
api.config.from_object(Config)
db = SQLAlchemy(api)

from api import routes, models

