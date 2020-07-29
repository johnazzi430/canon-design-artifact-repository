import os
from flask import Blueprint, Flask, current_app, send_file, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

from .clientApp import client_bp
from .config import Config

app = Flask(__name__, static_folder="../client/dist/static")
app.config.from_object(os.environ["APP_SETTINGS"])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)  # for serializing json output

from .modules.api import api
from .modules.auth import auth

static = Blueprint("static", __name__, static_folder="../client/dist/static")

app.register_blueprint(static)
app.register_blueprint(api)
# app.register_blueprint(auth)

app.logger.info(">>> {}".format(Config.FLASK_ENV))

cors = CORS(app, resources={r"/api/*": {"origins": "*"},})



@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def index_client(path):
    dist_dir = current_app.config["DIST_DIR"]
    entry = os.path.join(dist_dir, "index.html")
    return send_file(entry)
