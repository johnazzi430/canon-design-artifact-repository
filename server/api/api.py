import os
import secrets
import json
import sqlite3
import psycopg2
import sys
import mimetypes
from datetime import timedelta
from flask import Flask , flash, redirect, render_template, session, g
from flask import Blueprint, jsonify, request, current_app
from flask import send_file, make_response
from flask_cors import CORS
import sqlalchemy
from sqlalchemy import and_
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta
from functools import wraps
import jwt
import base64
import io
from .models import *


######

api = Blueprint('api_bp', __name__,url_prefix='/api')

# Session Settings
@api.before_request
def make_session_permanent():
    session.permanent = True
    api.permanent_session_lifetime = timedelta(minutes=1)

def user_in_session(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        try:
            user_id = session['user']
        except:
            return jsonify({"message" : "user not in session"})

        return f(*args, **kwargs)
    return decorated


##-------------------------- PERSONA API

## GET ALL
@api.route("/persona", methods = ['GET'])
@user_in_session
def persona_table():
    if request.args.get('filter') == "False" :
        personas = Persona.query.order_by(Persona.id).all()
        return json.dumps(PersonaSchema(exclude=['persona_picture']).dump(personas,many=True))
    else:
        personas = Persona.query.order_by(Persona.id).filter(Persona.archived.is_(False)).all()
        return json.dumps(PersonaSchema(exclude=['persona_picture']).dump(personas,many=True))

## GET PERSONA LIST

@api.route("/personas", methods = ['GET'])
@user_in_session
def persona_list():
#    personas = db.engine.execute("SELECT id as persona_id, name as persona_name, title as persona_title FROM PERSONA WHERE archived = False")
    personas = Persona.query.order_by(Persona.id).filter(Persona.archived.is_(False)).all()
    return json.dumps(PersonaSchema(only=['id','name','title']).dump(personas,many=True))

## GET BY ID

@api.route("/persona/<int:id>" , methods = ['GET'])
@user_in_session
def persona_table_by_id(id):
    persona = Persona.query.filter(Persona.id == id) \
            .options(joinedload('roles') ,joinedload('products') ) \
            .all()
    return json.dumps(PersonaSchema(exclude=['persona_picture']).dump(persona,many=True))


## POST NEW

@api.route("/persona" , methods = ['POST'])
@user_in_session
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
                creator_id = session['user'],
                access_group = 0,           # access_group TODO
                persona_maturity = session['persona_maturity'],
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



@api.route("/persona/<int:id>" , methods = ['PUT'])
@user_in_session
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
                creator_id = session['user'],
                action = 'edited '+ key,
                downchange = downchange,
                upchange = upchange)
    db.session.add(persona_comments)
    db.session.commit()
    return request.json, 201


##-------------------------- FILE API

@api.route("/persona/files/<int:id>" , methods = ['GET'])
@user_in_session
def personas_file_get(id):
    if request.args.get('file_id') != None:
        file = PersonaFile.query \
                .filter(PersonaFile.id == request.args.get('file_id')) \
                .first()
        response = make_response(file.file)
        response.headers.set( 'Content-Type', mimetypes.guess_type(file.filename))
        response.headers.set( 'Content-Disposition', 'attachment', filename=file.filename)
        return response
    else:
        files = PersonaFile.query \
                .with_entities(PersonaFile.id , PersonaFile.filename , PersonaFile.filetype) \
                .filter(PersonaFile.source_id == id).all()
        return json.dumps(PersonaFileSchema(only=['id','filename','filetype']).dump(files,many=True))

@api.route("/persona/files/<int:id>" , methods = ['POST'])
@user_in_session
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
@user_in_session
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
@user_in_session
def persona_get_roles():
    persona_roles = PersonaRoles.query.all()
    return json.dumps(PersonaRoleSchema().dump(persona_roles,many=True))


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

## AVATAR

@api.route("/persona/avatar/<int:id>" , methods = ['GET'])
# @user_in_session
def personas_avatar_download(id):
    try:
        persona = Persona.query.filter(Persona.id == id).first()
        response = make_response(persona.persona_picture)
        response.headers.set('Content-Type', 'image/jpeg')
        response.headers.set('Content-Disposition', 'inline')
        return response , 201
    except:
        return "no avatar found" , 404

@api.route("/persona/avatar/<int:id>" , methods = ['PUT'])
@user_in_session
def personas_avatar_upload(id):
    persona = Persona.query.filter(Persona.id == id).first()
    print(request.files)
    persona.persona_picture = request.files['file'].read()
    db.session.commit()
    return 'success', 201



##-------------------------- PRODUCT API

## GET PRODUCT LIST
@api.route("/products", methods = ['GET'])
@user_in_session
def product_list():
    products = Product.query.order_by(Product.id).filter(Product.archived.is_(False)).all()
    return json.dumps(ProductSchema(only=['id','name']).dump(products,many=True))

## GET ALL
@api.route("/product", methods = ['GET'])
@user_in_session
def product_table():
    if request.args.get('filter') == "False" :
        products = Product.query.order_by(Product.id).all()
        return json.dumps(ProductSchema().dump(products,many=True))
    else:
        products = Product.query.order_by(Product.id).filter(Product.archived.is_(False)).all()
        return json.dumps(ProductSchema().dump(products,many=True))

## GET BY ID
@api.route("/product/<int:id>" , methods = ['GET'])
@user_in_session
def product_table_by_id(id):
    products = Product.query.filter(Product.id == id) \
            .options(joinedload('personas')) \
            .all()
    return json.dumps(ProductSchema().dump(products,many=True))



@api.route("/product" , methods = ['POST'])
@user_in_session
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
                product_life = request.json['product_life'] ,
                creator_id = session['user'])
    if request.json.get('personas') != None:
        personas =[]
        for persona in request.json['personas']:
            personas.append(Persona.query.get(persona['id']))
        product.personas = personas

    db.session.add(product)
    db.session.commit()
    return request.json, 201


@api.route("/product/<int:id>" , methods = ['PUT'])
@user_in_session
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
                creator_id = session['user'],
                action = 'edited '+ key,
                downchange = downchange,
                upchange = upchange)
    db.session.add(product_comments)
    db.session.commit()
    return request.json, 201

##-------------------------- FILE API

@api.route("/product/files/<int:id>" , methods = ['GET'])
@user_in_session
def product_file_get(id):
    if request.args.get('file_id') != None:
        file = ProductFile.query \
                .filter(ProductFile.id == request.args.get('file_id')) \
                .first()
        response = make_response(file.file)
        response.headers.set('Content-Type', 'multipart/form-data ')
        response.headers.set( 'Content-Disposition', 'attachment', filename=file.filename)
        return response
    else:
        files = ProductFile.query \
                .with_entities(ProductFile.id , ProductFile.filename , ProductFile.filetype) \
                .filter(ProductFile.source_id == id).all()
        return json.dumps(ProductFileSchema(only=['id','filename','filetype']).dump(files,many=True))

@api.route("/product/files/<int:id>" , methods = ['POST'])
@user_in_session
def product_file_upload(id):
    file = ProductFile(
            source_id = id,
            file = request.files['file'].read(),
            filename = request.files['file'].filename,
            filetype = request.files['file'].filename.rsplit('.', 1)[1].lower())
    db.session.add(file)
    db.session.commit()
    return 'success', 201

@api.route("/product/files/<int:id>" , methods = ['DELETE'])
@user_in_session
def product_file_delete(id):
    if request.args.get('file_id') != None:
        file = ProductFile.query \
                .filter(ProductFile.id == request.args.get('file_id')) \
                .first()
        db.session.delete(file)
        db.session.flush()
        db.session.commit()
        return 'success', 201
    else:
        return 'A file id must be selected' , 404


##-------------------------- INSIGHTS API

## GET ALL
@api.route("/insights", methods = ['GET'])
@user_in_session
def insights_get():
    insights = Insight.query.order_by(Insight.id).filter(Insight.archived.is_(False)).all()
    return json.dumps(InsightSchema().dump(insights,many=True))

## GET BY ID
@api.route("/insights/<int:id>" , methods = ['GET'])
@user_in_session
def insights_get_by_id(id):
    insight = Insight.query.filter(Insight.id == id )\
                .options(joinedload('personas') ,joinedload('products') ) \
                .all()
    return json.dumps(InsightSchema().dump(insight,many=True))

## POST NEW
@api.route("/insights" , methods = ['POST'])
@user_in_session
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
            personas.append(Persona.query.get(persona['id']))
        insight.personas = personas

    db.session.add(insight)
    db.session.commit()
    return request.json, 201


@api.route("/insights/<int:id>" , methods = ['PUT'])
@user_in_session
def insights_put(id):
    data = request.get_json()
    key = list(data.keys())[0]
    insight = Insight.query.filter(Insight.id == id).first()

    ## Relatonships
    if key == 'personas':
        personas = []
        for persona in request.json['personas']:
            personas.append(Persona.query.get(persona['id']))
        insight.personas = personas
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
@user_in_session
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
        files = InsightFile.query \
                .with_entities(InsightFile.id , InsightFile.filename , InsightFile.filetype) \
                .filter(InsightFile.source_id == id).all()
        return json.dumps(InsightFileSchema(only=['id','filename','filetype']).dump(files,many=True))

@api.route("/insights/files/<int:id>" , methods = ['POST'])
@user_in_session
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
@user_in_session
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
@user_in_session
def persona_comments(id):
    persona_comments = PersonaComments.query.filter(PersonaComments.source_id == id).all()
    return json.dumps(PersonaCommentsSchema().dump(persona_comments,many=True))

@api.route("/product/comments/<int:id>" , methods = ['GET'])
@user_in_session
def product_comments(id):
    product_comments = ProductComments.query.filter(ProductComments.source_id == id).all()
    return json.dumps(ProductCommentsSchema().dump(product_comments,many=True))


@api.route("/insights/comments/<int:id>" , methods = ['GET'])
@user_in_session
def insights_comments(id):
    insight_comments = InsightComments.query.filter(InsightComments.source_id == id).all()
    return json.dumps(InsightCommentsSchema().dump(insight_comments,many=True))


## COMMENT ADD
@api.route("/persona/comments/<int:id>" , methods = ['POST'])
@user_in_session
def persona_comments_post(id):
    persona_comments = PersonaComments(                          ## SET ID
                source_id = id,
                comment_body= request.json['comment_body'],
                creator_id = session['user'],
                action = None,
                downchange = None,
                upchange = None)
    db.session.add(persona_comments)
    db.session.commit()
    return request.json, 201

@api.route("/product/comments/<int:id>" , methods = ['POST'])
@user_in_session
def product_comments_post(id):
    product_comments = ProductComments(                          ## SET ID
                source_id = id,
                comment_body= request.json['comment_body'],
                creator_id = session['user'],
                action = None,
                downchange = None,
                upchange = None)
    db.session.add(product_comments)
    db.session.commit()
    return request.json, 201

@api.route("/insights/comments/<int:id>" , methods = ['POST'])
@user_in_session
def insight_comments_post(id):
    insight_comments = InsightComments(                          ## SET ID
                source_id = id,
                comment_body= request.json['comment_body'],
                creator_id = session['user'])
    db.session.add(insight_comments)
    db.session.commit()
    return request.json, 201


#### Playlist ---------------------------------------------

@api.route("/playlist" , methods = ['GET'])
@user_in_session
def user_playlist():

    if not session['user']:
        return "No user logged in";

    if request.args.get('details') == 'True' :
        user_id = session['user']
        playlist = Playlist.query.filter(Playlist.user_id == user_id).all()
        response = []
        for play_item in playlist:
            source = play_item.source_table
            source_id = play_item.source_id
            if source == 'persona':
                persona = Persona.query.filter(Persona.id == source_id).first()
                data = PersonaSchema(only={'id','name','title','quote','avatar'}).dump(persona)
                data.update({"source" : source})
                response.append(data) ## # TODO: make this better

            if source == 'product':
                product = Product.query.filter(Product.id == source_id).first()
                data = ProductSchema(only={'id','name','description'}).dump(product)
                data.update({"source" : source})
                response.append(data)

            if source == 'insight':
                insight = Insight.query.filter(Insight.id == source_id).first()
                data = InsightSchema(only={'id','title','description','experience_vector'}).dump(insight)
                data.update({"source" : source})
                response.append(data)
        return json.dumps(response), 201
    else:
        user_id = session['user']
        playlist = Playlist.query.filter(Playlist.user_id == user_id).all()
        return json.dumps(PlaylistSchema().dump(playlist,many=True))

@api.route("/playlist" , methods = ['POST'])
@user_in_session
def add_to_playlist():
    if not request.args.get('source_table'):
        return "Missing source_table agrument", 404
    if not request.args.get('source_id'):
        return "Missing source_id agrument", 404
    if not session['user']:
        return "Missing user_id agrument", 404


    playlist_item= Playlist(
                user_id = session['user'],
                source_id = request.args.get('source_id'),
                source_table = request.args.get('source_table'),
                order = None)
    db.session.add(playlist_item)
    db.session.commit()
    return "Added to user playlist", 201

@api.route("/playlist" , methods = ['DELETE'])
@user_in_session
def remove_from_playlist():
    if not request.args.get('source_table'):
        return "Missing source_table agrument", 404
    if not request.args.get('source_id'):
        return "Missing source_id agrument", 404
    if not session['user']:
        return "Missing user_id agrument", 404

    playlist_item = Playlist.query.filter(and_(
                Playlist.user_id == session['user'],
                Playlist.source_id == request.args.get('source_id'),
                Playlist.source_table == request.args.get('source_table'))) \
            .first()

    db.session.delete(playlist_item)
    db.session.commit()
    return "Removed from user playlist", 201


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

# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = request.args.get('token')
#
#         if not token:
#             return jsonify({"message" : "token is missing"})
#
#         try:
#             data = jwt.decode(token, app_config['SECRET_KEY'])
#         except:
#             return jsonify({"message" : "token is invalid"})
#
#         return f(*args, **kwargs)
#     return decorated

from werkzeug.security import generate_password_hash , check_password_hash


@api.route('/test', methods = ['GET'])
@user_in_session
def protected():
    foo = "foo"
    return 'did it work?'

@api.route('/login', methods = ['POST'])
def authenticate_user():
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter(sqlalchemy.func.lower(User.username) == username.lower()).first() ## force lowercase filter
    if not user or not user.verify_password(password) or not user.role:
        return jsonify( { 'username': username , 'authenticated' : False} ) , 401

    token = jwt.encode({ 'username': username, "exp" : datetime.now() + timedelta(minutes=30)},current_app.config['SECRET_KEY'])
    session['user'] = user.user_id
    user_json = UserSchema(only=("username","user_id","role")).dump(user)
    return jsonify( {"token" : token.decode('UTF-8') , "user" : user_json }) , 200

@api.route('/logout', methods = ['POST'])
def clear_session():
    session.pop('user', None)
    return "logged out"

## Lets admins change role
@api.route('/refresh', methods = ['GET'])
def refresh_token():
    request.json.get('username')
    user = User.query.filter_by(username == username).first()
    g.user = user
    token = jwt.encode({ 'username': username, "exp" : datetime.now() + timedelta(minutes=30)},current_app.config['SECRET_KEY'])
    return jsonify( {"token" : token.decode('UTF-8')})

## lets users register
@api.route('/users', methods = ['POST'])
def add_user():
    username = request.json.get('username').lower()
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

## Lets users change their own password
@api.route('/users', methods = ['PUT'])
def change_password():
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

## checks if user is in session
@api.route('/users', methods = ['GET'])
@user_in_session
def get_user_data():
    if request.args.get('session') == 'true':
        # GET current user info
        try:
            user_id = session['user']
            print(user_id)
            user = User.query.filter_by(user_id = user_id).all()
            return json.dumps(UserSchema(only=("username","user_id","role")).dump(user,many=True))
        except:
            return "no user logged in"
    else:
        # GET everything
        users = User.query.all()
        return json.dumps(UserSchema(only=("username","user_id","role")).dump(users,many=True))

## gets user data by id
@api.route('/users/<int:user_id>', methods = ['GET'])
@user_in_session
def get_user_data_by_id(user_id):
    user = User.query.filter_by(user_id = user_id).all()
    return json.dumps(UserSchema(only=("username","user_id","role")).dump(user,many=True))

## Lets admins change role
@api.route('/users/<int:user_id>', methods = ['PUT'])
@user_in_session
def admin_change_user(user_id):
    data = request.get_json()
    user = User.query.filter_by(user_id = user_id).first()
    for key in list(data.keys()):
        setattr(user, key , data[key]) #SET UPCHANGE
    db.session.commit()
    return request.json, 201

## Lets admins reset password
@api.route('/users/<int:user_id>/password-reset', methods = ['PUT'])
@user_in_session
def reset_user_password(user_id):
    user = User.query.filter_by(user_id = user_id).first()
    new_password = 'password123'
    user.hash_password(new_password)
    db.session.commit()

    token = jwt.encode({ 'username': user.username, "exp" : datetime.now() + timedelta(minutes=30)},current_app.config['SECRET_KEY'])
#    return jsonify( { 'username': username , 'authenticated' : True , 'role': user.role } )
    return jsonify( {"token" : token.decode('UTF-8') , "user" : user.username})
