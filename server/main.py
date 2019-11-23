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

def create_table():
    c.execute("""CREATE TABLE PERSONA (
            id integer,
            name text,
            title text,
            quote text,
            function text,
            needs text,
            wants text,
            pain_point text,
            persona_file blob,
            record_date text,
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

## GET BY ID
@app.route("/api/persona-table/<int:id>" , methods = ['GET'])
def persona_table_by_id(id):
    with sqlite3.connect('server/data/data.db') as conn:
        c = conn.cursor()
        result = c.execute("SELECT * FROM PERSONA WHERE id = :id ", {'id' : id})
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

# @app.route("/edit-form/<int:id>" , methods=('GET', 'POST'))
# def create_new():
#     c.execute("SELECT * as last_id FROM PERSONA WHERE id = :id ", {'id' : id})).fetchall()[-1][0]
#     data = [dict(zip([key[0] for key in c.description], row)) for row in result]
#     form = Persona_Input(obj=data)
#     if form.validate_on_submit():
#         with sqlite3.connect('server/data/data.db') as conn:
#             c = conn.cursor()
#             last_rev = c.execute("SELECT MAX(revision) as last_id FROM PERSONA WHERE id = :id ", {'id' : id})).fetchall()[0][0]
#             data = [id,form.name.data , form.title.data ,form.quote.data ,form.function.data ,form.needs.data ,form.wants.data ,form.pain_point.data , form.persona_file.data, datetime.datetime.now(),last_rev ]
#             c.execute("""INSERT INTO PERSONA VALUES (?,?,?,?,?,?,?,?,?,?,?)""",data)
#             conn.commit()
# ##          return redirect('/')
#             return redirect("/home")
#     return render_template("edit-form.html", form = form )

##--------------------------------------
 

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=5000 , debug=True)
