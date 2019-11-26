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



##-------------------------- PERSONA API

## GET ALL
@app.route("/")
@app.route("/api/persona-table", methods = ['GET'])
def persona_table():
    if request.args.get('filter') == "False" :
        with sqlite3.connect('server/data/data.db') as conn:
            c = conn.cursor()
            result = c.execute("SELECT * FROM PERSONA") # TODO: WHERE archived = 0
            data = [dict(zip([key[0] for key in c.description], row)) for row in result]
            return json.dumps(data)
    else :
        with sqlite3.connect('server/data/data.db') as conn:
            c = conn.cursor()
            ## ONLY GET THE LAST REVISION WHERE NOT ARCHIVED
            result = c.execute("""SELECT
                                PERSONA.*
                            FROM
                                ( SELECT
                                    name,
                                    MAX(revision) as last_revision
                                FROM PERSONA
                                GROUP BY name) AS LAST
                            INNER JOIN
                                PERSONA
                            ON
                                PERSONA.name = LAST.name AND
                                PERSONA.revision = LAST.last_revision
                            WHERE
                                PERSONA.archived = 0""")
            data = [dict(zip([key[0] for key in c.description], row)) for row in result]
            return json.dumps(data)

## POST NEW
@app.route("/api/persona-table" , methods = ['POST'])
def persona_post():
    app.logger.info(request.json['name'])
    with sqlite3.connect('server/data/data.db') as conn:
        c = conn.cursor()
        last_id = c.execute("SELECT MAX(id) as last_id FROM PERSONA ").fetchall()[0][0]
        last_revision = c.execute("SELECT IFNULL(MAX(revision),0)+1 as last_revision FROM PERSONA where name=?", [request.json['name']]).fetchall()[0][0]
        data = [last_id+1,                              ## SET ID
                request.json['name'],
                request.json['title'] ,
                request.json['quote'],
                request.json['job_function'] ,
                request.json['needs'] ,
                request.json['wants'] ,
                request.json['pain_point'] ,
                request.json['external'] ,
                request.json['market_size'] ,
                request.json['buss_val'] ,
                datetime.datetime.now(),               # Record Date
                last_revision,                          # Revision
                None,                                # creator_id   TODO
                None,                                # access_group TODO
                0,                                     # archived
                request.json['persona_file']]

        c.execute("""INSERT INTO PERSONA
        (id,
        name,
        title,
        quote,
        job_function,
        needs,
        wants,
        pain_point,
        external,
        market_size,
        buss_val,
        record_date,
        revision,
        creator_id,
        access_group,
        archived,
        persona_file)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",data)
        return request.json, 201

## GET BY ID
@app.route("/api/persona-table/<int:id>" , methods = ['GET'])
def persona_table_by_id(id):
    with sqlite3.connect('server/data/data.db') as conn:
        c = conn.cursor()
        result = c.execute("SELECT * FROM PERSONA WHERE id = :id ", {'id' : id})
        data = [dict(zip([key[0] for key in c.description], row)) for row in result]
        return json.dumps(data)


@app.route("/api/persona-table/<int:id>" , methods = ['PUT'])
def persona_table_put_by_id(id):
    app.logger.info(request.json)

    SQL = "UPDATE PERSONA SET "
    data_values = []
    # Iterate through JSON object nad build SQL query
    for item in request.json:
        attribute = item
        value = request.json[item]
        SQL = SQL +" "+ attribute + " = " + "?" +" "
        data_values.append(value)

    SQL = SQL + " WHERE id = ?"
    data_values.append(id)
    app.logger.info(SQL)
    app.logger.info(data_values)
    with sqlite3.connect('server/data/data.db') as conn:
        c = conn.cursor()
        c.execute( SQL, data_values)
        return request.json, 201


##-------------------------- PRODUCT API

## GET ALL
@app.route("/api/product-table", methods = ['GET'])
def product_table():
    with sqlite3.connect('server/data/data.db') as conn:
        c = conn.cursor()
        result = c.execute("SELECT * FROM PRODUCT") # TODO: WHERE archived = 0
        data = [dict(zip([key[0] for key in c.description], row)) for row in result]
        return json.dumps(data)

## POST NEW
@app.route("/api/product-table" , methods = ['POST'])
def product_post():
    app.logger.info(request.json['name'])
    with sqlite3.connect('server/data/data.db') as conn:
        c = conn.cursor()
        last_id = c.execute("SELECT MAX(id) as last_id FROM PRODUCT ").fetchall()[0][0]
        last_revision = c.execute("SELECT IFNULL(MAX(revision),0)+1 as last_revision FROM PRODUCT where name=?", [request.json['name']]).fetchall()[0][0]
        data = [last_id+1,                              ## SET ID
                request.json['name'],
                request.json['title'] ,
                request.json['quote'],
                request.json['job_function'] ,
                request.json['needs'] ,
                request.json['wants'] ,
                request.json['pain_point'] ,
                request.json['external'] ,
                request.json['market_size'] ,
                request.json['buss_val'] ,
                datetime.datetime.now(),               # Record Date
                datetime.datetime.now(),               # Record Date
                last_revision,                          # Revision
                None,                                # creator_id   TODO
                None,                                # access_group TODO
                0,                                     # archived
                request.json['persona_file'],
                request.json['persona_picture']]

        c.execute("""INSERT INTO PRODUCT
        (id,
        name,
        title,
        quote,
        job_function,
        needs,
        wants,
        pain_point,
        external,
        market_size,
        buss_val,
        create_date,
        last_update_date
        revision,
        creator_id,
        access_group,
        archived,
        persona_file,
        persona_picture)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?.?)""",data)
        return request.json, 201

## GET BY ID
@app.route("/api/product-table/<int:id>" , methods = ['GET'])
def product_table_by_id(id):
    with sqlite3.connect('server/data/data.db') as conn:
        c = conn.cursor()
        result = c.execute("SELECT * FROM PRODUCT WHERE id = :id ", {'id' : id})
        data = [dict(zip([key[0] for key in c.description], row)) for row in result]
        return json.dumps(data)


@app.route("/api/product-table/<int:id>" , methods = ['PUT'])
def product_table_put_by_id(id):
    app.logger.info(request.json)

    SQL = "UPDATE PRODUCT SET "
    data_values = []
    # Iterate through JSON object nad build SQL query
    for item in request.json:
        attribute = item
        value = request.json[item]
        SQL = SQL +" "+ attribute + " = " + "?" +" "
        data_values.append(value)

    SQL = SQL + " WHERE id = ?"
    data_values.append(id)
    app.logger.info(SQL)
    app.logger.info(data_values)
    with sqlite3.connect('server/data/data.db') as conn:
        c = conn.cursor()
        c.execute( SQL, data_values)
        return request.json, 201


@app.route("/api/comments/<table>/<int:id>" , methods = ['GET'])
def comments_by_table_and_item(table,id):
    with sqlite3.connect('server/data/data.db') as conn:
        c = conn.cursor()
        result = c.execute("SELECT * FROM COMMENTS WHERE source_id = ? AND source_table = ? ", [ id , table])
        data = [dict(zip([key[0] for key in c.description], row)) for row in result]
        return json.dumps(data)

# TODO: Make this work
@app.route("/api/comments/<table>/<int:id>" , methods = ['POST'])
def comments_create_by_table_and_item(table,id):
    with sqlite3.connect('server/data/data.db') as conn:
        c = conn.cursor()
        result = c.execute("SELECT * FROM COMMENTS WHERE source_id = ? AND source_table = ? ", [ id , table])
        data = [dict(zip([key[0] for key in c.description], row)) for row in result]
        return json.dumps(data)



##--------------------------------------


if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=5000 , debug=True)
