import os
import secrets
import json
import sqlite3
import datetime
from flask import Flask , flash, redirect, render_template, session
from flask import Blueprint, jsonify, request, current_app
from flask_cors import CORS
from sqlite3 import Error


api = Blueprint('api_bp', __name__,url_prefix='/api')

## ---------------- SERVE STATIC
#
# @api.route('/', defaults={'path': ''})
# @api.route('/<path:path>')
# def catch_all(path):
#     if app.debug:
#         return requests.get('http://localhost:8080/{}'.format(path)).text
#     return render_template("index.html")
#
#


##-------------------------- PERSONA API


## METHODS
def convertToBinaryData(filename):
    #Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


## GET ALL
@api.route("/persona-table", methods = ['GET'])
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

## GET PERSONA LIST
@api.route("/personas", methods = ['GET'])
def persona_list():
    with sqlite3.connect('server/data/data.db') as conn:
        c = conn.cursor()
        result = c.execute("SELECT id as value , title as text FROM PERSONA") # TODO: WHERE archived = 0
        data = [dict(zip([key[0] for key in c.description], row)) for row in result]
        return json.dumps(data)



## POST NEW
@api.route("/persona-table" , methods = ['POST'])
def persona_post():
    current_app.logger.info(request.json['name'])
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
                request.json['persona_file'],
                request.json['persona_picture']]

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
        create_date,
        revision,
        creator_id,
        access_group,
        archived,
        persona_file,
        persona_picture)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",data)
        conn.commit()
        return request.json, 201

## GET BY ID
@api.route("/persona-table/<int:id>" , methods = ['GET'])
def persona_table_by_id(id):
    with sqlite3.connect('server/data/data.db') as conn:
        c = conn.cursor()
        persona = c.execute("SELECT * FROM PERSONA WHERE id = :id ", {'id' : id})
        data = [dict(zip([key[0] for key in persona.description], row)) for row in persona]
        if id != 0:
            persona_products = c.execute("""SELECT
                                                PERS_PROD_REL.product_id as product_id,
                                                PRODUCT.name as product_name
                                        FROM PERS_PROD_REL
                                        INNER JOIN PRODUCT ON PRODUCT.id = PERS_PROD_REL.product_id
                                        WHERE persona_id = :id """, {'id' : id})
            data_add = [dict(zip([key[0] for key in persona.description], row)) for row in persona_products]
            data[0]['product'] = data_add
            return json.dumps(data), 201
        else:
            return json.dumps([{'id': None}])


@api.route("/persona-table/<int:id>" , methods = ['PUT'])
def persona_table_put_by_id(id):
    current_app.logger.info(request.json)

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
    current_app.logger.info(SQL)
    current_app.logger.info(data_values)
    with sqlite3.connect('server/data/data.db') as conn:
        c = conn.cursor()
        c.execute( SQL, data_values)
        conn.commit()
        return request.json, 201


##-------------------------- PRODUCT API

## GET PRODUCT LIST
@api.route("/products", methods = ['GET'])
def product_list():
    with sqlite3.connect('server/data/data.db') as conn:
        c = conn.cursor()
        result = c.execute("SELECT id as value, name as text FROM PRODUCT") # TODO: WHERE archived = 0
        data = [dict(zip([key[0] for key in c.description], row)) for row in result]
        return json.dumps(data)


## GET ALL
@api.route("/product-table", methods = ['GET'])
def product_table():
    with sqlite3.connect('server/data/data.db') as conn:
        c = conn.cursor()
        result = c.execute("SELECT * FROM PRODUCT") # TODO: WHERE archived = 0
        data = [dict(zip([key[0] for key in c.description], row)) for row in result]
        return json.dumps(data)

## POST NEW
@api.route("/product-table" , methods = ['POST'])
def product_post():
    current_app.logger.info(request.json['name'])
    with sqlite3.connect('server/data/data.db') as conn:
        c = conn.cursor()
        last_id = c.execute("SELECT MAX(id) as last_id FROM PRODUCT ").fetchall()[0][0]
        last_revision = c.execute("SELECT IFNULL(MAX(revision),0)+1 as last_revision FROM PRODUCT where name=?", [request.json['name']]).fetchall()[0][0]
        data = [last_id+1,                              ## SET ID
                request.json['name'],
                request.json['description'] ,
                request.json['metrics'],
                request.json['goals'] ,
                request.json['features'] ,
                datetime.datetime.now(),               # Record Date
                datetime.datetime.now(),               # Record Date
                0,                                     # archived
                None,                                # creator_id   TODO
                request.json['owner'],                                # access_group TODO
                last_revision,                          # Revision
                request.json['product_homepage']        ]

        c.execute("""INSERT INTO PRODUCT
        (id,
        name,
        description,
        metrics,
        goals,
        features,
        create_date,
        last_update,
        archived,
        creator_id,
        owner,
        revision,
        product_homepage)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",data)
        return request.json, 201

## GET BY ID
@api.route("/product-table/<int:id>" , methods = ['GET'])
def product_table_by_id(id):
    with sqlite3.connect('server/data/data.db') as conn:
        c = conn.cursor()
        result = c.execute("SELECT * FROM PRODUCT WHERE id = :id ", {'id' : id})
        data = [dict(zip([key[0] for key in c.description], row)) for row in result]
        return json.dumps(data)


@api.route("/product-table/<int:id>" , methods = ['PUT'])
def product_table_put_by_id(id):
    current_app.logger.info(request.json)

    SQL = "UPDATE PRODUCT SET "
    data_values = []
    # Iterate through JSON object nad build SQL query
    for item in request.json:
        attribute = item
        value = request.json[item]
        SQL = SQL +" "+ attribute + " = " + "?" +" "
        data_values.append(value)

    SQL = SQL + " WHERE id = ?"
    current_app.logger.info(SQL)
    data_values.append(id)
    with sqlite3.connect('server/data/data.db') as conn:
        c = conn.cursor()
        c.execute( SQL, data_values)
        conn.commit()
        return request.json, 201


@api.route("/persona/comments/<int:id>" , methods = ['GET'])
def persona_comments(id):
    with sqlite3.connect('server/data/data.db') as conn:
        c = conn.cursor()
        result = c.execute("SELECT * FROM PERSONA_COMMENTS WHERE source_id = ?", [id] )
        data = [dict(zip([key[0] for key in c.description], row)) for row in result]
        return json.dumps(data)

@api.route("/product/comments/<int:id>" , methods = ['GET'])
def product_comments(id):
    with sqlite3.connect('server/data/data.db') as conn:
        c = conn.cursor()
        result = c.execute("SELECT * FROM PRODUCT_COMMENTS WHERE source_id = ?", [id] )
        data = [dict(zip([key[0] for key in c.description], row)) for row in result]
        return json.dumps(data)


## COMMENTS
@api.route("/persona/comments/<int:id>" , methods = ['POST'])
def persona_comments_post(id):
    with sqlite3.connect('server/data/data.db') as conn:
        c = conn.cursor()
        last_id = c.execute("SELECT MAX(id) as last_id FROM PERSONA_COMMENTS ").fetchall()[0][0]
        data = [
            last_id+1,
            request.json['source_id'],
            request.json['comment_body'],
            None,       #creator id # TODO:
            datetime.datetime.now(),
            request.json['action'],
            request.json['downchange'],
            request.json['upchange']]
        c.execute("""INSERT INTO PERSONA_COMMENTS
        (id,
        source_id,
        comment_body,
        creator_id,
        create_date,
        action,
        downchange,
        upchange)
        VALUES (?,?,?,?,?,?,?,?)""",data)
        return request.json, 201
        return json.dumps(data)

@api.route("/product/comments/<int:id>" , methods = ['POST'])
def product_comments_post(id):
    with sqlite3.connect('server/data/data.db') as conn:
        c = conn.cursor()
        last_id = c.execute("SELECT MAX(id) as last_id FROM PRODUCT_COMMENTS ").fetchall()[0][0]
        data = [
            last_id+1,
            request.json['source_id'],
            request.json['comment_body'],
            None,       #creator id # TODO:
            datetime.datetime.now(),
            request.json['action'],
            request.json['downchange'],
            request.json['upchange']]
        c.execute("""INSERT INTO PRODUCT_COMMENTS
        (id,
        source_id,
        comment_body,
        creator_id,
        create_date,
        action,
        downchange,
        upchange)
        VALUES (?,?,?,?,?,?,?,?)""",data)
        return request.json, 201
        return json.dumps(data)

## PERSONA TO PRODUCT REL Table




## TODO MAKE WORK
@api.route("/persona-product-relationship/" , methods = ['GET'])
def persona_product_relationship_get():
    if request.args.get('persona_id') != None and request.args.get('product_id') == None:
        SQL = "SELECT * FROM PERS_PROD_REL WHERE persona_id = :id"
        id = request.args.get('persona_id')
    elif request.args.get('product_id') != None and request.args.get('persona_id') == None:
        SQL = "SELECT * FROM PERS_PROD_REL WHERE product_id = :id"
        id = request.args.get('product_id')
    else:
        SQL = "SELECT * FROM PERS_PROD_REL"
        id = None

    with sqlite3.connect('server/data/data.db') as conn:
        c = conn.cursor()
        result = c.execute("SELECT * FROM PERS_PROD_REL")
        #result = c.execute("SELECT * FROM PERS_PROD_REL WHERE id = :id ", {'id' : id})
        data = [dict(zip([key[0] for key in c.description], row)) for row in result]
        return json.dumps(data)


@api.route("/persona-product-relationship" , methods = ['POST'])
def persona_product_rel_post():
    with sqlite3.connect('server/data/data.db') as conn:
        c = conn.cursor()
        data = [last_id+1,                              ## SET ID
                request.json['name'],
                request.json['title'] ,
                request.json['quote']]
#        c.execute("""INSERT INTO PRODUCT"""
        return request.json, 201



## AUTHORIZATION
from werkzeug.security import generate_password_hash , check_password_hash

@api.route('/users/auth', methods = ['POST'])
def authenticate_user():
    username = request.json.get('username')
    password = request.json.get('password')
    # if username is None or password is None:
    #     return "missing information"
    with sqlite3.connect('server/data/data.db') as conn:
        c = conn.cursor()
        result = c.execute("SELECT username, password_hash FROM USERS where username =?" , [username]).fetchall()
        if result != [] and check_password_hash(result[0],password) == True:
            return jsonify( { 'username': username , 'authenticated' : True} )
        else:
            return jsonify( { 'username': username , 'authenticated' : False} )
#
@api.route('/users', methods = ['POST'])
def add_user():
    username = request.json.get('username')
    password = request.json.get('password')
    password_hash = generate_password_hash(password)
    with sqlite3.connect('server/data/data.db') as conn:
        c = conn.cursor()
        check_username = (c.execute("SELECT user_id FROM USERS where username =?" , [username]).fetchall() == [])
        if check_username == True:
            last_id = c.execute("SELECT MAX(user_id) as last_id FROM USERS ").fetchall()[0][0]
            data = [ last_id +1 , username , password_hash , None]
            c.execute(""" INSERT INTO USERS (user_id,username,password_hash,role) VALUES (?,?,?,?)""" , data)
            return jsonify( { 'username': username  , 'authenticated' : True} )
        else:
            return 'this user already exists'


@api.route('/users', methods = ['PUT'])
def reset_password():
    username = request.json.get('username')
    current_password = request.json.get('current_password')
    new_password = request.json.get('new_password')
    password_hash = generate_password_hash(new_password)
    with sqlite3.connect('server/data/data.db') as conn:
        c = conn.cursor()
        result = c.execute("SELECT username, password_hash FROM USERS where username =?" , [username]).fetchall()
        if check_password_hash(result[0][1], current_password ) == True:
            c = conn.cursor()
            c.execute("UPDATE USERS  SET password_hash = ? WHERE username = ?", [ password_hash , username ])
            return jsonify( { 'username': username  , 'authenticated' : True , 'password_changed' : True} )
        else:
            return 'password incorrect'
