import os
from flask import Flask, current_app, send_file, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

from .clientApp import client_bp
from .config import Config

app = Flask(__name__,static_folder='../client/dist/static')
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)  # for serializing json output

from .api.api import api
from .api.auth import auth

app.register_blueprint(api)
app.register_blueprint(auth)

app.logger.info('>>> {}'.format(Config.FLASK_ENV))

cors = CORS(app, resources={
                    r"/api/*": {"origins": "*"},
                    })
cors = CORS(app, resources={
                    r"/auth/*": {"origins": "*"},
                    })

@app.route('/')
def index_client():
    dist_dir = current_app.config['DIST_DIR']
#    entry = os.path.join(dist_dir, 'index.html')
    entry = os.path.join(dist_dir, 'index.html')
    return send_file(entry)



### SSO TEST
from flask import Flask, session, redirect
from flask_sso import SSO

sso = SSO(app=app)
SSO_ATTRIBUTE_MAP = {
    'ADFS_EMAIL': (True, 'email')
    }
    


app.config['SSO_ATTRIBUTE_MAP'] = SSO_ATTRIBUTE_MAP

@sso.login_handler
def login_callback(user_info):
    """Store information in session."""
    session['user'] = user_info

@app.route('/sso_test')
def index():
    """Display user information or force login."""
    if 'user' in session:
        return 'Welcome {name}'.format(name=session['user']['nickname'])
    return redirect(app.config['SSO_LOGIN_URL'])
