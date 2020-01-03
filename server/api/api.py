import os
import secrets
import json
import sqlite3
import psycopg2
import sys
from flask import Flask , flash, redirect, render_template, session, g
from flask import Blueprint, jsonify, request, current_app
from flask import send_file, make_response
from flask_cors import CORS
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta
from functools import wraps
import jwt
import base64
import io
from .models import *


api = Blueprint('api_bp', __name__,url_prefix='/api')

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

@api.route("/persona/files/<int:id>" , methods = ['DELETE'])
def persona_file_delete(id):
    if request.args.get('file_id') != None:
        file = PersonaFile.query \
                .filter(PersonaFile.id == request.args.get('file_id')) \
                .first()
        db.session.delete(file)
        db.session.flush()
        db.session.commit()
        return 'success', 201
    else:
        return 'A file id must be selected' , 404

@api.route("/persona/roles" , methods = ['GET'])
def persona_get_roles():
    persona_roles = PersonaRoles.query.all()
    return json.dumps(PersonaRoleSchema().dump(persona_roles,many=True))

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
        downchange = getattr(insight, key) #GET DOWNCHANGE
        setattr(insight, key , upchange) #SET UPCHANGE
    setattr(insight, 'revision' ,insight.revision + 1)
    db.session.commit()
    return request.json, 201


@api.route("/insights/files/<int:id>" , methods = ['GET'])
def insights_file_get(id):
    if request.args.get('file_id') != None:
        file = InsightFile.query \
                .filter(InsightFile.id == request.args.get('file_id')) \
                .first()
        response = make_response(file.file)
        response.headers.set('Content-Type', 'multipart/form-data ')
        response.headers.set( 'Content-Disposition', 'attachment', filename=file.filename)
        return response
    else:
        files = InsightFile.query.filter(InsightFile.source_id == id).all()
        return json.dumps(insightFileSchema(only=['id','filename','filetype']).dump(files,many=True))

@api.route("/insights/files/<int:id>" , methods = ['POST'])
def insights_file_upload(id):
    file = InsightFile(
            source_id = id,
            file = request.files['file'].read(),
            filename = request.files['file'].filename,
            filetype = request.files['file'].filename.rsplit('.', 1)[1].lower())
    db.session.add(file)
    db.session.commit()
    return 'success', 201

@api.route("/insights/files/<int:id>" , methods = ['DELETE'])
def insight_file_delete(id):
    if request.args.get('file_id') != None:
        file = InsightFile.query \
                .filter(InsightFile.id == request.args.get('file_id')) \
                .first()
        db.session.delete(file)
        db.session.flush()
        db.session.commit()
        return 'success', 201
    else:
        return 'A file id must be selected' , 404



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


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({"message" : "token is missing"})

        try:
            data = jwt.decode(token, app_config['SECRET_KEY'])
        except:
            return jsonify({"message" : "token is invalid"})

        return f(*args, **kwargs)
    return decorated

@api.route('/login', methods = ['GET'])
@token_required
def protected():
    foo = "foo"
    return 'did it work?'

@api.route('/login', methods = ['POST'])
def authenticate_user():
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username = username).first()
    if not user or not user.verify_password(password) or not user.role:
        return jsonify( { 'username': username , 'authenticated' : False} ) , 401
    g.user = user
    token = jwt.encode({ 'username': username, "exp" : datetime.now() + timedelta(minutes=30)},current_app.config['SECRET_KEY'])
#    return jsonify( { 'username': username , 'authenticated' : True , 'role': user.role } )
    return jsonify( {"token" : token.decode('UTF-8') , "username" : username, "role" : user.role}) , 200

@api.route('/refresh', methods = ['GET'])
@token_required
def refresh_token():
    request.json.get('username')
    user = User.query.filter_by(username = username).first()
    g.user = user
    token = jwt.encode({ 'username': username, "exp" : datetime.now() + timedelta(minutes=30)},current_app.config['SECRET_KEY'])
    return jsonify( {"token" : token.decode('UTF-8')})

#
@api.route('/users', methods = ['POST'])
def add_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    if User.query.filter_by(username = username).first() is not None:
        abort(400) # existing user
    user = User(username = username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify( { 'username': username  , 'authenticated' : True} )


## TODO NOT WORKING?
@api.route('/users', methods = ['PUT'])
def reset_password():
    username = request.json.get('username')
    current_password = request.json.get('current_password')
    new_password = request.json.get('new_password')
    user = User.query.filter_by(username = username).first()
    if not user or not user.verify_password(current_password) or not user.role:
        return jsonify( { 'message': "current password incorrect"} )
    user.hash_password(new_password)
    db.session.commit()

    token = jwt.encode({ 'username': username, "exp" : datetime.now() + timedelta(minutes=30)},current_app.config['SECRET_KEY'])
#    return jsonify( { 'username': username , 'authenticated' : True , 'role': user.role } )
    return jsonify( {"token" : token.decode('UTF-8') , "user" : username})

@api.route('/users', methods = ['GET'])
def get_user_data():
    users = User.query.all()
    return json.dumps(UserSchema(only=("username","user_id","role")).dump(users,many=True))

@api.route('/users/<int:user_id>', methods = ['GET'])
def get_user_data_by_id(user_id):
    user = User.query.filter_by(user_id = user_id).all()
    return json.dumps(UserSchema(only=("username","user_id","role")).dump(user,many=True))


@api.route('/users/<int:user_id>', methods = ['PUT'])
def admin_user(user_id):
    data = request.get_json()
    user = User.query.filter_by(user_id = user_id).first()
    for key in list(data.keys()):
        setattr(user, key , data[key]) #SET UPCHANGE
    db.session.commit()
    return request.json, 201
