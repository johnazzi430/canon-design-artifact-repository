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
from sqlalchemy.orm import joinedload
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
    return json.dumps(PersonaSchema(only=['id','name','title']).dump(personas,many=True))

## GET BY ID
@api.route("/persona-table/<int:id>" , methods = ['GET'])
def persona_table_by_id(id):
    persona = Persona.query.filter(Persona.id == id) \
            .options(joinedload('roles') ,joinedload('products') ) \
            .all()
    return json.dumps(PersonaSchema().dump(persona,many=True))


## POST NEW
@api.route("/persona-table" , methods = ['POST'])
def persona_post():
    persona = Persona(                          ## SET ID
                name = request.json['name'],
                title = request.json['title'] ,
                quote = request.json['quote'],
                job_function = request.json['job_function'] ,
                needs = request.json['needs'] ,
                wants = request.json['wants'] ,
                pain_point = request.json['pain_point'] ,
                external = request.json['external'] ,
                market_size = request.json['market_size'] ,
                buss_val = request.json['buss_val'] ,
                revision = 0,                          # Revision
                creator_id = None,          # creator_id   TODO
                access_group = 0,           # access_group TODO
                persona_file = None,
                persona_picture = None)

    if request.json.get('roles') != None:
        roles = []
        for role in request.json['roles']:
            roles.append(PersonaRoles.query.get(role['id']))
        persona.roles = roles

    if request.json.get('products') != None:
        products =[]
        for product in request.json['products']:
            products.append(Product.query.get(product['id']))
        persona.products = products

    db.session.add(persona)
    db.session.commit()
    return request.json, 201



@api.route("/persona-table/<int:id>" , methods = ['PUT'])
def persona_table_put_by_id(id):

    data = request.get_json()
    key = list(data.keys())[0]
    persona = Persona.query.filter(Persona.id == id).first()

    if key == 'roles':
        roles = []
        for role in request.json['roles']:
            roles.append(PersonaRoles.query.get(role['id']))
        persona.roles = roles
        upchange = ""
        downchange = ""
    elif key == 'products' :
        products =[]
        for product in request.json['products']:
            products.append(Product.query.get(product['id']))
        persona.products = products
        upchange = ""
        downchange = ""
    else:
        upchange = data[key]
        downchange = getattr(persona, key) #GET DOWNCHANGE
        setattr(persona, key , upchange) #SET UPCHANGE

    ## Add comment to log changes and edits
    setattr(persona, 'revision' , persona.revision + 1)
    persona_comments = PersonaComments(                          ## SET ID
                source_id = id,
                comment_body= None,
                creator_id = None,
                action = 'edited '+ key,
                downchange = downchange,
                upchange = upchange)
    db.session.add(persona_comments)
    db.session.commit()
    return request.json, 201


##-------------------------- FILE API


@api.route("/persona/files/<int:id>" , methods = ['GET'])
def personas_file_get(id):
    if request.args.get('file_id') != None:
        file = PersonaFile.query \
                .filter(PersonaFile.id == request.args.get('file_id')) \
                .first()
        response = make_response(file.file)
        response.headers.set('Content-Type', 'multipart/form-data ')
        response.headers.set( 'Content-Disposition', 'attachment', filename=file.filename)
        return response
    else:
        files = PersonaFile.query.filter(PersonaFile.source_id == id).all()
        return json.dumps(PersonaFileSchema(only=['id','filename','filetype']).dump(files,many=True))

@api.route("/persona/files/<int:id>" , methods = ['POST'])
def personas_file_upload(id):
    file = PersonaFile(
            source_id = id,
            file = request.files['file'].read(),
            filename = request.files['file'].filename,
            filetype = request.files['file'].filename.rsplit('.', 1)[1].lower())
    db.session.add(file)
    db.session.commit()
    return 'success', 201



## TODO: delete files

##-------------------------- PRODUCT API



## GET PRODUCT LIST
@api.route("/products", methods = ['GET'])
def product_list():
    products = Product.query.order_by(Product.id).filter(Product.archived.is_(False)).all()
    return json.dumps(ProductSchema(only=['id','name']).dump(products,many=True))

## GET ALL
@api.route("/product-table", methods = ['GET'])
def product_table():
    if request.args.get('filter') == "False" :
        products = Product.query.order_by(Product.id).all()
        return json.dumps(ProductSchema().dump(products,many=True))
    else:
        products = Product.query.order_by(Product.id).filter(Product.archived.is_(False)).all()
        return json.dumps(ProductSchema().dump(products,many=True))

## GET BY ID
@api.route("/product-table/<int:id>" , methods = ['GET'])
def product_table_by_id(id):
    products = Product.query.filter(Product.id == id) \
            .options(joinedload('personas')) \
            .all()
    return json.dumps(ProductSchema().dump(products,many=True))



@api.route("/product-table" , methods = ['POST'])
def product_post():
    current_app.logger.info(request.json['name'])
    product = Product(                          ## SET ID
                name = request.json['name'],
                description = request.json['description'] ,
                metrics = request.json['metrics'],
                goals = request.json['goals'] ,
                features = request.json['features'] ,
                owner = request.json['owner'],
                product_homepage = request.json['product_homepage'] ,
                creator_id = None)
    if request.json.get('personas') != None:
        personas =[]
        for persona in request.json['personas']:
            personas.append(Personas.query.get(persona['id']))
        product.personas = personas

    db.session.add(product)
    db.session.commit()
    return request.json, 201


@api.route("/product-table/<int:id>" , methods = ['PUT'])
def product_table_put_by_id(id):
    data = request.get_json()
    key = list(data.keys())[0]
    product = Product.query.filter(Product.id == id).first()

    if key == 'personas':
        personas = []
        for persona in request.json['personas']:
            personas.append(Persona.query.get(persona['id']))
        product.roles = roles
        upchange = ""
        downchange = ""
    else:
        upchange = data[key]
        downchange = getattr(product, key) #GET DOWNCHANGE
        setattr(product, key , upchange) #SET UPCHANGE

    ## Add comment to log changes and edits
    setattr(product, 'revision' , product.revision + 1)
    product_comments = ProductComments(                          ## SET ID
                source_id = id,
                comment_body= None,
                creator_id = None,
                action = 'edited '+ key,
                downchange = downchange,
                upchange = upchange)
    db.session.add(product_comments)
    db.session.commit()
    return request.json, 201

##-------------------------- INSIGHTS API

## GET ALL
@api.route("/insights", methods = ['GET'])
def insights_get():
    insights = Insight.query.order_by(Insight.id).filter(Insight.archived.is_(False)).all()
    return json.dumps(InsightSchema().dump(insights,many=True))

## GET BY ID
@api.route("/insights/<int:id>" , methods = ['GET'])
def insights_get_by_id(id):
    insight = Insight.query.filter(Insight.id == id )\
                .options(joinedload('personas') ,joinedload('products') ) \
                .all()
    return json.dumps(InsightSchema().dump(insight,many=True))

## POST NEW
@api.route("/insights" , methods = ['POST'])
def insights_post():
    current_app.logger.info(request.json['title'])
    insight = Insight(
            title = request.json['title'],
            description = request.json['description'] ,
            content = request.json['content'],
            file = request.json['file'],                                   # content file
            experience_vector = request.json['experience_vector'] ,
            magnitude = request.json['magnitude'] ,
            frequency = request.json['frequency'] ,
            emotions = request.json['emotions'] ,
            props = request.json['props'] ,
            journey = request.json['journey'])

    ## Relatonships
    if request.json.get('products') != None:
        products =[]
        for product in request.json['products']:
            products.append(Product.query.get(product['id']))
        insight.products = products

    if request.json.get('personas') != None:
        personas =[]
        for persona in request.json['personas']:
            personas.append(Personas.query.get(persona['id']))
        insight.personas = personas

    db.session.add(insight)
    db.session.commit()
    return request.json, 201


@api.route("/insights/<int:id>" , methods = ['PUT'])
def insights_put(id):
    data = request.get_json()
    key = list(data.keys())[0]
    insight = Insight.query.filter(Insight.id == id).first()

    ## Relatonships
    if key == 'personas':
        personas = []
        for persona in request.json['personas']:
            personas.append(Persona.query.get(persona['id']))
        insight.roles = roles
        upchange = ""
        downchange = ""
    elif key == 'products' :
        products =[]
        for product in request.json['products']:
            products.append(Product.query.get(product['id']))
        insight.products = products
        upchange = ""
        downchange = ""
    else:
        upchange = data[key]
        downchange = getattr(persona, key) #GET DOWNCHANGE
        setattr(persona, key , upchange) #SET UPCHANGE
    setattr(insight, 'revision' ,insight.revision + 1)

    ## Add comment to log changes and edits
    insight_comments = InsightComments(                          ## SET ID
                source_id = id,
                comment_body= None,
                creator_id = None,
                action = 'edited '+ key,
                downchange = downchange,
                upchange = upchange)
    db.session.add(insight_comments)
    db.session.commit()
    return request.json, 201



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
    persona_comments = PersonaComments.query.filter(PersonaComments.source_id == id).all()
    return json.dumps(PersonaCommentsSchema().dump(persona_comments,many=True))

@api.route("/product/comments/<int:id>" , methods = ['GET'])
def product_comments(id):
    product_comments = ProductComments.query.filter(ProductComments.source_id == id).all()
    return json.dumps(ProductCommentsSchema().dump(product_comments,many=True))


@api.route("/insights/comments/<int:id>" , methods = ['GET'])
def insights_comments(id):
    insight_comments = InsightComments.query.filter(InsightComments.source_id == id).all()
    return json.dumps(InsightCommentsSchema().dump(insight_comments,many=True))


## COMMENT ADD
@api.route("/persona/comments/<int:id>" , methods = ['POST'])
def persona_comments_post(id):
    persona_comments = PersonaComments(                          ## SET ID
                source_id = id,
                comment_body= request.json['comment_body'],
                creator_id = None,
                action = None,
                downchange = None,
                upchange = None)
    db.session.add(persona_comments)
    db.session.commit()
    return request.json, 201

@api.route("/product/comments/<int:id>" , methods = ['POST'])
def product_comments_post(id):
    product_comments = ProductComments(                          ## SET ID
                source_id = id,
                comment_body= request.json['comment_body'],
                creator_id = None,
                action = None,
                downchange = None,
                upchange = None)
    db.session.add(product_comments)
    db.session.commit()
    return request.json, 201

@api.route("/insights/comments/<int:id>" , methods = ['POST'])
def insight_comments_post(id):
    insight_comments = InsightComments(                          ## SET ID
                source_id = id,
                comment_body= request.json['comment_body'],
                creator_id = None,
                action = None,
                downchange = None,
                upchange = None)
    db.session.add(insight_comments)
    db.session.commit()
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
