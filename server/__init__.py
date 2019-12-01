import os
from flask import Flask, current_app, send_file, render_template
from flask_cors import CORS

from .api.api import api
from .clientApp import client_bp


app = Flask(__name__,
    static_folder='../client/dist/static')
app.register_blueprint(api)
# app.register_blueprint(client_bp)

from .config import Config
app.logger.info('>>> {}'.format(Config.FLASK_ENV))

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/')
def index_client():
    dist_dir = current_app.config['DIST_DIR']
#    entry = os.path.join(dist_dir, 'index.html')
    entry = os.path.join(dist_dir, 'index.html')
    return send_file(entry)
