import os
import secrets
import json
import sqlite3
import psycopg2
import datetime
import sys
from flask import Flask , flash, redirect, render_template, session
from flask import Blueprint, jsonify, request, current_app
from flask import send_file, make_response
from flask_cors import CORS
from sqlite3 import Error
import base64
import io
from .models import *


api = Blueprint('api_bp', __name__,url_prefix='/api')

## define database connection - should be moved to config
def db_connect():
#    conn = psycopg2.connect(host="localhost",dbname="test", user="postgres", password="mypass01", port=5111)
    conn = sqlite3.connect('server/data/data.db')
    return conn

# pgloader

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
        personas = Persona.query.order_by(Persona.id).all()
        return json.dumps(PersonaSchema().dump(personas,many=True))
    else:
        personas = Persona.query.order_by(Persona.id).filter(Persona.archived.is_(False)).all()
        return json.dumps(PersonaSchema().dump(personas,many=True))

## GET PERSONA LIST
@api.route("/personas", methods = ['GET'])
def persona_list():
#    personas = db.engine.execute("SELECT id as persona_id, name as persona_name, title as persona_title FROM PERSONA WHERE archived = False")
    personas = Persona.query.order_by(Persona.id).filter(Persona.archived.is_(False)).all()
    return json.dumps(PersonaSchema(only=['id,name,tile']).dump(personas,many=True))


## POST NEW
@api.route("/persona-table" , methods = ['POST'])
def persona_post():
    current_app.logger.info(request.json['name'])
    persona = Persona(                          ## SET ID
                name = request.json['name'],
                title = request.json['title'] ,
                quote = request.json['quote'])
                # job_function = request.json['job_function'] ,
                # needs = request.json['needs'] ,
                # wants = request.json['wants'] ,
                # pain_point = request.json['pain_point'] ,
                # external = request.json['external'] ,
                # market_size = request.json['market_size'] ,
                # buss_val = request.json['buss_val'] ,
                # create_date = datetime.now(),               # Record Date
                # revision = 0,                          # Revision
                # creator_id = None,          # creator_id   TODO
                # access_group = 0,           # access_group TODO
                # archived = False,      # archived
                # persona_file = request.json['persona_file'],
                # persona_picture = request.json['persona_picture'])
    db.session.add(persona)
    db.session.commit()
    return request.json, 201

## GET BY ID
@api.route("/persona-table/<int:id>" , methods = ['GET'])
def persona_table_by_id(id):
    with db_connect() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM PERSONA WHERE id = %s", (id,))
        persona = c.fetchall()
        data = [dict(zip([key[0] for key in persona.description], row)) for row in persona]
        if id != 0 or id != None:
            c.execute("""SELECT
                                        PERS_PROD_REL.product_id as product_id,
                                        PRODUCT.name as product_name
                                        FROM PERS_PROD_REL
                                        INNER JOIN PRODUCT ON PRODUCT.id = PERS_PROD_REL.product_id
                                        WHERE persona_id = %s""", (id,))
            persona_products = c.fetchall()
            data_add = [dict(zip([key[0] for key in persona.description], row)) for row in persona_products]
            data[0]['products'] = data_add
            c.execute("""SELECT
                                        PERSONA_ROLES_REL.persona_role_id as persona_role_id,
                                        PERSONA_ROLES.name as persona_role_name
                                        FROM PERSONA_ROLES_REL
                                        INNER JOIN PERSONA_ROLES ON PERSONA_ROLES.id = PERSONA_ROLES_REL.persona_role_id
                                        WHERE persona_id = %s""", (id,))
            persona_roles = c.fetchall()
            data_add = [dict(zip([key[0] for key in persona.description], row)) for row in persona_roles]
            data[0]['roles'] = data_add
            return json.dumps(data), 201
        else:
            return json.dumps([{'id': None}])


@api.route("/persona-table/<int:id>" , methods = ['PUT'])
def persona_table_put_by_id(id):
    data = request.get_json()
    key = list(data.keys())[1]
        #has to take an index of a list of keys because we dont know what the key that is changing is
        #we could modify the json being sent from the front end but idk
    value = data[key]
    with db_connect() as conn:
        c = conn.cursor()
        SQL = "UPDATE PERSONA SET " + key + " = ? WHERE id = ? "
        # SQL = SQL + "OUTPUT inserted.{}"
        #
        # SQL = """UPDATE PERSONA SET {} = ? WHERE id = ?
        #         OUTPUT inserted.{}
        #                inserted.persona_id
        #                deleted.{}
        #                INTO PERSONA_COMMENTS"
        #
        data_values = [value , data['id']]
        c.execute(SQL,data_values)
        conn.commit()
    return request.json, 201


##-------------------------- FILE API

### TODO: WORKS! BUT NEEDS A LOT OF CLEANUP
@api.route("/persona/files/<int:id>" , methods = ['GET'])
def personas_file_get(id):
    with db_connect() as conn:
        c = conn.cursor()
        if request.args.get('file_id') != None:
            file_id = int(request.args.get('file_id'))
            c.execute("""SELECT filename, file FROM PERSONA_FILES WHERE id = ?""",[file_id])
            record = c.fetchall()
            filename = record[0][0]
            file = record[0][1]
            response = make_response(file)
            response.headers.set('Content-Type', 'multipart/form-data ')
            response.headers.set(
                    'Content-Disposition', 'attachment', filename=filename)
            return response
        else:
            #Return a Json containing the file descriptions
            c.execute("""SELECT id,filename,filetype,source_id FROM PERSONA_FILES WHERE source_id = %s""",(id,))
            record = c.fetchall()
            data = [dict(zip([key[0] for key in c.description], row)) for row in record]
            return json.dumps(data)


@api.route("/persona/files/<int:id>" , methods = ['POST'])
def personas_file_upload(id):
    print(request.files['file'])
    with db_connect() as conn:
        c = conn.cursor()
        file = request.files["file"].read() #BLOB the data
        filename = request.files["file"].filename
        filetype = filename.rsplit('.', 1)[1].lower()
        last_id = c.execute("SELECT MAX(id) as last_id FROM PERSONA_FILES ").fetchall()[0][0]
        c.execute("""INSERT INTO PERSONA_FILES
            (id,filename,file,filetype,source_id)
            VALUES (?,?,?,?,?)""",[last_id+1,filename,file,filetype,id])
        conn.commit()
        return 'success', 201

## TODO: delete files

##-------------------------- PRODUCT API



## GET PRODUCT LIST
@api.route("/products", methods = ['GET'])
def product_list():
    products = Product.query.order_by(Product.id).filter(Product.archived.is_(False)).all()
    return json.dumps(ProductSchema(only=['id,name']).dump(products,many=True))

## GET ALL
@api.route("/product-table", methods = ['GET'])
def product_table():
    if request.args.get('filter') == "False" :
        products = Product.query.order_by(Product.id).all()
        return json.dumps(ProductSchema().dump(products,many=True))
    else:
        products = Product.query.order_by(Product.id).filter(Product.archived.is_(False)).all()
        return json.dumps(ProductSchema().dump(products,many=True))

## POST NEW
@api.route("/product-table" , methods = ['POST'])
def product_post():
    current_app.logger.info(request.json['name'])
    with db_connect() as conn:
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
        conn.commit()
        return request.json, 201

## GET BY ID
@api.route("/product-table/<int:id>" , methods = ['GET'])
def product_table_by_id(id):
    products = Product.query.order_by(Product.id).filter(Product.id == id).all()
    return json.dumps(ProductSchema().dump(products,many=True))



@api.route("/product-table/<int:id>" , methods = ['PUT'])
def product_table_put_by_id(id):
    data = request.get_json()
    key = list(data.keys())[1]
        #has to take an index of a list of keys because we dont know what the key that is changing is
        #we could modify the json being sent from the front end but idk
    value = data[key]
    with db_connect() as conn:
        c = conn.cursor()
        SQL = "UPDATE PRODUCT SET " + key + " = ? WHERE id = ? "
        data_values = [value , data['id']]
        c.execute(SQL,data_values)
        conn.commit()
    return request.json, 201

##-------------------------- INSIGHTS API


## GET ALL
@api.route("/insights", methods = ['GET'])
def insights_get():
    with db_connect() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM INSIGHT WHERE archived = False") # TODO: WHERE archived = 0
        result = c.fetchall()
        data = [dict(zip([key[0] for key in c.description], row)) for row in result]
        return json.dumps(data)

## POST NEW
@api.route("/insights" , methods = ['POST'])
def insights_post():
    current_app.logger.info(request.json['title'])
    with db_connect() as conn:
        c = conn.cursor()
        last_id = c.execute("SELECT MAX(id) as last_id FROM INSIGHT ").fetchall()[0][0]
        last_revision = c.execute("SELECT IFNULL(MAX(revision),0)+1 as last_revision FROM INSIGHT where title=?", [request.json['title']]).fetchall()[0][0]
        data = [last_id+1,                              ## SET ID
                request.json['title'],
                request.json['description'] ,
                request.json['content'],
                request.json['file'],                                   # content file
                request.json['experience_vector'] ,
                request.json['magnitude'] ,
                request.json['frequency'] ,
                request.json['emotions'] ,
                request.json['props'] ,
                request.json['journey'] ,
                request.json['creator_id'],
                datetime.datetime.now(),               # Record Date
                last_revision,
                0]                                     # archived
        c.execute("""INSERT INTO INSIGHT
        (id,
        title,
        description,
        content,
        file,
        experience_vector,
        magnitude,
        frequency,
        emotions,
        props,
        journey,
        creator_id,
        create_date,
        revision,
        archived)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",data)
        conn.commit()
        return request.json, 201

## GET BY ID
@api.route("/insights/<int:id>" , methods = ['GET'])
def insights_get_by_id(id):
    with db_connect() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM INSIGHT WHERE id = ? ", [id])
        result = c.fetchall()
        data = [dict(zip([key[0] for key in c.description], row)) for row in result]
        return json.dumps(data)


@api.route("/insights/<int:id>" , methods = ['PUT'])
def insights_put(id):
    data = request.get_json()
    key = list(data.keys())[1]
        #has to take an index of a list of keys because we dont know what the key that is changing is
        #we could modify the json being sent from the front end but idk
    value = data[key]
    with db_connect() as conn:
        c = conn.cursor()
        SQL = "UPDATE INSIGHT SET " + key + " = ? WHERE id = ? "
        data_values = [value , data['id']]
        c.execute(SQL,data_values)
        conn.commit()
    return request.json, 201

## relationshops
# TODO: this
@api.route("/insights/<int:id>/<table>" , methods = ['GET'])
def insights_get_relationship(id,table):
    with db_connect() as conn:
        c = conn.cursor()
        if table == 'products':
            c.execute("""SELECT
                                                PRODUCT.id as product_id,
                                                PRODUCT.name as product_name
                                            FROM INSIGHT
                                            INNER JOIN INSIGHT_PRODUCT_REL on INSIGHT_PRODUCT_REL.insight_id = INSIGHT.id
                                            INNER JOIN PRODUCT ON PRODUCT.id = INSIGHT_PRODUCT_REL.product_id
                                            WHERE INSIGHT.id = ? """, [id])
            insight_products = c.fetchall()
            data = [dict(zip([key[0] for key in insight_products.description], row)) for row in insight_products]
            return json.dumps(data)
        elif table == 'personas':
            insight_personas = c.execute("""SELECT
                                                PERSONA.id as persona_id,
                                                PERSONA.title as persona_title
                                            FROM INSIGHT
                                            INNER JOIN INSIGHT_PERSONA_REL on INSIGHT_PERSONA_REL.insight_id = INSIGHT.id
                                            INNER JOIN PERSONA ON PERSONA.id = INSIGHT_PERSONA_REL.persona_id
                                            WHERE INSIGHT.id = ? """, [id])
            insight_personas = c.fetchall()
            data = [dict(zip([key[0] for key in insight_personas.description], row)) for row in insight_personas]
            return json.dumps(data)
        else:
            return 'error' ,  401


@api.route("/insights/<int:id>/<table>" , methods = ['POST'])
def insights_post_relationship(id,table):
    with db_connect() as conn:
        c = conn.cursor()
        if table == 'products':
            c.execute( "DELETE FROM INSIGHT_PRODUCT_REL WHERE insight_id = ?;" , [id])
            data =[]
            for item in request.json:
                data.append([item['product_id'],id])
            c.executemany("INSERT INTO INSIGHT_PRODUCT_REL (product_id,insight_id) VALUES (?,?)",data)
            conn.commit()
            return 'success', 201
        elif table == 'personas':
            c.execute( "DELETE FROM INSIGHT_PERSONA_REL WHERE insight_id = ?;" , [id])
            data =[]
            for item in request.json:
                data.append([item['persona_id'],id])
            c.executemany("INSERT INTO INSIGHT_PERSONA_REL (persona_id,insight_id) VALUES (?,?)",data)
            conn.commit()
            return 'success', 201
        else:
            return 'error' ,  401

@api.route("/insights/<int:id>/files" , methods = ['GET'])
def insight_file_get(id):
    with db_connect() as conn:
        c = conn.cursor()
        if request.args.get('file_id') != None:
            file_id = int(request.args.get('file_id'))
            record = c.execute("""SELECT filename, file FROM INSIGHT_FILES WHERE id = ?""",[file_id]).fetchall()
            filename = record[0][0]
            file = record[0][1]
            response = make_response(file)
            response.headers.set('Content-Type', 'multipart/form-data ')
            response.headers.set(
                    'Content-Disposition', 'attachment', filename='%s.jpg' % id)
            return response
        else:
            #Return a Json containing the file descriptions
            c.execute("""SELECT id,filename,filetype,source_id FROM INSIGHT_FILES WHERE source_id = ?""",[id])
            record = c.fetchall()
            data = [dict(zip([key[0] for key in c.description], row)) for row in record]
            return json.dumps(data)


@api.route("/insights/<int:id>/files" , methods = ['POST'])
def insight_file_upload(id):
    print(request.files['file'])
    with db_connect() as conn:
        c = conn.cursor()
        file = request.files["file"].read() #BLOB the data
        filename = request.files["file"].filename
        filetype = filename.rsplit('.', 1)[1].lower()
        last_id = c.execute("SELECT MAX(id) as last_id FROM INSIGHT_FILES ").fetchall()[0][0]
        c.execute("""INSERT INTO INSIGHT_FILES
            (id,filename,file,filetype,source_id)
            VALUES (?,?,?,?,?)""",[last_id+1,filename,file,filetype,id])
        conn.commit()
        return 'success', 201



#### COMMENTS ---------------------------------------------
@api.route("/persona/comments/<int:id>" , methods = ['GET'])
def persona_comments(id):
    with db_connect() as conn:
        c = conn.cursor()
        result = c.execute("SELECT * FROM PERSONA_COMMENTS WHERE source_id = ?", [id] )
        data = [dict(zip([key[0] for key in c.description], row)) for row in result]
        return json.dumps(data)

@api.route("/product/comments/<int:id>" , methods = ['GET'])
def product_comments(id):
    with db_connect() as conn:
        c = conn.cursor()
        result = c.execute("SELECT * FROM PRODUCT_COMMENTS WHERE source_id = ?", [id] )
        data = [dict(zip([key[0] for key in c.description], row)) for row in result]
        return json.dumps(data)

@api.route("/insights/comments/<int:id>" , methods = ['GET'])
def insights_comments(id):
    with db_connect() as conn:
        c = conn.cursor()
        result = c.execute("SELECT * FROM INSIGHT_COMMENTS WHERE source_id = ?", [id] )
        data = [dict(zip([key[0] for key in c.description], row)) for row in result]
        return json.dumps(data)


## COMMENT ADD
@api.route("/persona/comments/<int:id>" , methods = ['POST'])
def persona_comments_post(id):
    with db_connect() as conn:
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
        conn.commit()
        return request.json, 201
        return json.dumps(data)

@api.route("/product/comments/<int:id>" , methods = ['POST'])
def product_comments_post(id):
    with db_connect() as conn:
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
        conn.commit()
        return request.json, 201
        return json.dumps(data)

@api.route("/insights/comments/<int:id>" , methods = ['POST'])
def insight_comments_post(id):
    with db_connect() as conn:
        c = conn.cursor()
        last_id = c.execute("SELECT MAX(id) as last_id FROM INSIGHT_COMMENTS ").fetchall()[0][0]
        data = [
            last_id+1,
            request.json['source_id'],
            request.json['comment_body'],
            None,       #creator id # TODO:
            datetime.datetime.now()]
        c.execute("""INSERT INTO INSIGHT_COMMENTS
            (id,
            source_id,
            comment_body,
            creator_id,
            create_date)
        VALUES (?,?,?,?,?)""",data)
        conn.commit()
        return request.json, 201
        return json.dumps(data)

###### PERSONA RELATIONSHIPS
@api.route("/persona-product" , methods = ['GET'])
def persona_product_relationship_get():
    if request.args.get('persona_id') != None and request.args.get('product_id') == None:
        SQL = "SELECT * FROM PERS_PROD_REL WHERE persona_id = :id;"
        id = request.args.get('persona_id')
    elif request.args.get('product_id') != None and request.args.get('persona_id') == None:
        SQL = "SELECT * FROM PERS_PROD_REL WHERE product_id = :id;"
        id = request.args.get('product_id')
    else:
        SQL = "SELECT * FROM PERS_PROD_REL"
        id = None

    with db_connect() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM PERS_PROD_REL")
        #result = c.execute("SELECT * FROM PERS_PROD_REL WHERE id = :id ", {'id' : id})
        result = c.fetchall()
        data = [dict(zip([key[0] for key in c.description], row)) for row in result]
        return json.dumps(data)


@api.route("/persona-product" , methods = ['POST'])
def persona_product_rel_post():
    with db_connect() as conn:
        c = conn.cursor()
        if request.args.get('table') == 'persona':
            id = request.json.get('id')
            c.execute( "DELETE FROM PERS_PROD_REL WHERE persona_id = ?;" , [id])
            data =[]
            for item in request.json.get('products'):
                 data.append([id,item['product_id']])
            c.executemany("INSERT INTO PERS_PROD_REL(persona_id,product_id) VALUES (?,?)",data)
            conn.commit()
            return request.json, 201
        elif request.args.get('table') == 'product':
            id = request.json.get('id')
            c.execute( "DELETE FROM PERS_PROD_REL WHERE product_id = ?;" , [id])
            data =[]
            for item in request.json.get('personas'):
                 data.append([item['persona_id'],id])
            c.executemany("INSERT INTO PERS_PROD_REL(persona_id,product_id) VALUES (?,?)",data)
            conn.commit()
            return request.json, 201
        else:
            return "error"

## pickup_roles
@api.route("/persona/roles" , methods = ['GET'])
def persona_roles_get():
    with db_connect() as conn:
        c = conn.cursor()
        c.execute("SELECT id as persona_role_id, name as persona_role_name FROM PERSONA_ROLES")
        result = c.fetchall()
        #result = c.execute("SELECT * FROM PERS_PROD_REL WHERE id = :id ", {'id' : id})
        data = [dict(zip([key[0] for key in c.description], row)) for row in result]
        return json.dumps(data)


@api.route("/persona/roles" , methods = ['POST'])
def persona_role_post():
    with db_connect() as conn:
        c = conn.cursor()
        id = request.json.get('id')
        c.execute( "DELETE FROM PERSONA_ROLES_REL WHERE persona_id = ?;" , [id])
        data =[]
        for item in request.json.get('roles'):
            data.append([id,item['persona_role_id']])
        c.executemany("INSERT INTO PERSONA_ROLES_REL (persona_id,persona_role_id) VALUES (?,?)",data)
        conn.commit()
        return request.json, 201

# PLACEHOLDER FOR API TO PUT NEW ROLES
# @api.route("/persona/roles" , methods = ['POST'])
# def persona_role_post():
#     with db_connect() as conn:
#         c = conn.cursor()
#         id = request.json.get('id')
#         c.execute( "DELETE FROM PERSONA_ROLES_REL WHERE persona_id = ?;" , [id])
#         data =[]
#         for item in request.json.get('roles'):
#             data.append([id,item['persona_role_id']])
#         c.executemany("INSERT INTO PERSONA_ROLES_REL (persona_id,persona_role_id) VALUES (?,?)",data)
#         conn.commit()
#         return request.json, 201


## AUTHORIZATION
from werkzeug.security import generate_password_hash , check_password_hash

@api.route('/users/auth', methods = ['POST'])
def authenticate_user():
    username = request.json.get('username')
    password = request.json.get('password')
    # if username is None or password is None:
    #     return "missing information"
    with db_connect() as conn:
        c = conn.cursor()
        result = c.execute("SELECT username, password_hash, role FROM USERS where username =?" , [username]).fetchall()
        conn.commit()
        if result != []:
            if check_password_hash(result[0][1],password) == True:
                return jsonify( { 'username': username , 'authenticated' : True , 'role': result[0][2]} )
            else:
                return jsonify( { 'username': username , 'authenticated' : False} )
        else:
            return jsonify( { 'username': username , 'authenticated' : False} )
#
@api.route('/users', methods = ['POST'])
def add_user():
    username = request.json.get('username')
    password = request.json.get('password')
    password_hash = generate_password_hash(password)
    with db_connect() as conn:
        c = conn.cursor()
        check_username = (c.execute("SELECT user_id FROM USERS where username =?" , [username]).fetchall() == [])
        if check_username == True:
            last_id = c.execute("SELECT MAX(user_id) as last_id FROM USERS ").fetchall()[0][0]
            data = [ last_id +1 , username , password_hash , None]
            c.execute(""" INSERT INTO USERS (user_id,username,password_hash,role) VALUES (?,?,?,?)""" , data)
            conn.commit()
            return jsonify( { 'username': username  , 'authenticated' : True} )
        else:
            return 'this user already exists'


## TODO NOT WORKING?
@api.route('/users', methods = ['PUT'])
def reset_password():
    username = request.json.get('username')
    current_password = request.json.get('current_password')
    new_password = request.json.get('new_password')
    password_hash = generate_password_hash(new_password)
    with db_connect() as conn:
        c = conn.cursor()
        result = c.execute("SELECT username, password_hash FROM USERS where username =?" , [username]).fetchall()
        if check_password_hash(result[0][1], current_password ) == True:
            c = conn.cursor()
            c.execute("UPDATE USERS  SET password_hash = ? WHERE username = ?", [ password_hash , username ])
            conn.commit()
            return jsonify( { 'username': username  , 'authenticated' : True , 'password_changed' : True} )
        else:
            return 'password incorrect'

@api.route('/users', methods = ['GET'])
def get_user_data():
    with db_connect() as conn:
        c = conn.cursor()
        result = c.execute("SELECT user_id , username, role FROM USERS ")
        data = [dict(zip([key[0] for key in c.description], row)) for row in result]
        return json.dumps(data)


@api.route('/users/admin', methods = ['PUT'])
def admin_user():
    username = request.json.get('username')
    new_role = request.json.get('role')
    if request.json.get('admin').lower() == 'admin':
        with db_connect() as conn:
            c = conn.cursor()
            c.execute("UPDATE USERS SET role = ? WHERE username = ?", [ new_role, username])
            conn.commit()
            return jsonify( { 'username': username  , 'role' : new_role})
    else:
        return "user must be an admin" , 401
