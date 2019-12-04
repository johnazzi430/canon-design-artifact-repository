import os
import secrets
import json
import sqlite3
import datetime
from flask import Flask , flash, redirect, render_template, session
from flask import Blueprint, jsonify, request, current_app
from flask_cors import CORS
from sqlite3 import Error

from werkzeug.security import generate_password_hash , check_password_hash


auth = Blueprint('auth_bp', __name__,url_prefix='/auth')

@auth.route('/users/auth', methods = ['POST'])
def authenticate_user():
    username = request.json.get('username')
    password = request.json.get('password')
    # if username is None or password is None:
    #     return "missing information"
    with sqlite3.connect('server/data/data.db') as conn:
        c = conn.cursor()
        result = c.execute("SELECT username, password_hash FROM USERS where username =?" , [username]).fetchall()
        if check_password_hash(result[0],password) == True:
            return jsonify( { 'username': username , 'authenticated' : True} )
        else:
            return jsonify( { 'username': username , 'authenticated' : False} )
#
@auth.route('/users', methods = ['POST'])
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


@auth.route('/users', methods = ['PUT'])
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
