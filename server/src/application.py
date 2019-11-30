from flask import Flask
from flask_cors import CORS

def create_app(app_name='PERSONA_API'):
  app = Flask(app_name)
  app.config.from_object('src.config.BaseConfig')

  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  from src.api import api
  app.register_blueprint(api, url_prefix="/api")


  return app
