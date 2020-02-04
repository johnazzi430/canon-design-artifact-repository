

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from server\api\models.py import *

engine = create_engine(r"sqlite:////Users\m317413\Desktop\3.programming\utc-persona-playbook\server\data\utcpersonaapp.db")
