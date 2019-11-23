import os
import secrets
import json
import sqlite3
import datetime
from flask import Flask , flash, request , redirect, render_template, jsonify, session
from flask_sso import SSO
from flask_cors import CORS
from sqlite3 import Error
from src.models import Persona
from src.forms import Persona_Input


app = Flask(__name__)
app.config['SECRET_KEY']  = r'_5#y2L"F4Q8z\n\xec]/'
app.config['CORS_HEADERS'] = 'Content-Type'
ext = SSO(app=app)

cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

SSO_ATTRIBUTE_MAP = {
    'ADFS_AUTHLEVEL': (False, 'authlevel'),
    'ADFS_GROUP': (True, 'group'),
    'ADFS_LOGIN': (True, 'nickname'),
    'ADFS_ROLE': (False, 'role'),
    'ADFS_EMAIL': (True, 'email'),
    'ADFS_IDENTITYCLASS': (False, 'external'),
    'HTTP_SHIB_AUTHENTICATION_METHOD': (False, 'authmethod'),
}

app.config['SSO_ATTRIBUTE_MAP'] = SSO_ATTRIBUTE_MAP



conn = sqlite3.connect('server/data/data.db')
c = conn.cursor()
# TODO:
def create_table():
    c.execute("""CREATE TABLE PERSONA (
            id integer,
            name text,
            title text,
            external integer,           NEW
            quote text,
            jobFunction text,           NEW
            needs text,
            wants text,
            pain_point text,
            buss_val integer,           NEW
            persona_file blob,
            record_date text,
            archived integer,           NEW
            creator_id text,            NEW
            access_group text,          NEW
            revision integer

            ) """)
    return


#TODO: Add in QTY field in table

##--------------------------

###

## GET ALL
@app.route("/")
@app.route("/api/persona-table", methods = ['GET'])
def persona_table():
    with sqlite3.connect('server/data/data.db') as conn:
        c = conn.cursor()
        result = c.execute("SELECT * FROM PERSONA ")
        data = [dict(zip([key[0] for key in c.description], row)) for row in result]
        return json.dumps(data)

## POST NEW
@app.route("/api/persona-table" , methods = ['POST'])
def persona_post():
    app.logger.info(request.json['name'])

    with sqlite3.connect('server/data/data.db') as conn:
        data = request
        c = conn.cursor()
        last_id = c.execute("SELECT MAX(id) as last_id FROM PERSONA ").fetchall()[0][0]
        data = [last_id+1,request.json['name'] , request.json['title'] ,request.json['quote'],request.json['jobFunction'] ,request.json['needs'] ,request.json['wants'] ,request.json['pain_point'] , request.json['persona_file'], datetime.datetime.now(),1 ]
        c.execute("""INSERT INTO PERSONA VALUES (?,?,?,?,?,?,?,?,?,?,?)""",data)
        return request.json, 201

## GET BY ID
@app.route("/api/persona-table/<int:id>" , methods = ['GET'])
def persona_table_by_id(id):
    with sqlite3.connect('server/data/data.db') as conn:
        c = conn.cursor()
        result = c.execute("SELECT * FROM PERSONA WHERE id = :id ", {'id' : id})
        data = [dict(zip([key[0] for key in c.description], row)) for row in result]
        return json.dumps(data)

## Update values
@app.route("/api/persona-table/<int:id>?<attribute>=<value>" , methods = ['PUT'])
def persona_table_put_by_id(id):
    return 201

    # app.logger.info(id)
    # app.logger.info(request.json)
    # with sqlite3.connect('server/data/data.db') as conn:
    #     c = conn.cursor()
    #     result = c.execute( """UPDATE PERSONA
    #                             SET :attribute = :value
    #                             WHERE id = :id""", { 'attribute' : attribute ,
    #                                                  'value' : value,
    #                                                  'id' : id })
    #     data = [dict(zip([key[0] for key in c.description], row)) for row in result]
    #     return request.json, 201

##--------------------------------------


if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=5000 , debug=True)
