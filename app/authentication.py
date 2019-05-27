import uuid
import jwt
import datetime
from flask import Flask, request, session, jsonify, make_response, Blueprint, \
                render_template, flash, redirect, url_for, request, jsonify, current_app, g
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from .models import *
from flask_httpauth import HTTPTokenAuth

auth = Blueprint("auth", __name__)
token_auth = HTTPTokenAuth()

@token_auth.verify_token
def verify_token(token):
    try:
        token_payload = jwt.decode(token, current_app.config['SECRET_KEY'])
        user = Account.query.filter_by(id = token_payload['id']).first()
        g.current_user = user if token else None
        return g.current_user is not None
    except:
        return False
    return False

@auth.route("/do-login", methods=["POST"])
def do_login():
    # Get data from the form input, check if they are valid 
    # and send login data to the login function

    username = request.form.get("username")
    password = request.form.get("password")

    return login(username, password)
    
def login(username, password):
    # See if a login is successful and return 
    # a valid JSON response
    if not username and not password:
        return jsonify({'success': False, 'message' : 'Invalid login request data'})

    login_token = get_login_token(username, password)

    if login_token == None:
        return jsonify({'success': False, 'message' : 'Invalid credentials'})

    session["token"] = login_token.decode('UTF-8')

    return jsonify({'success': True, 'token' : login_token.decode('UTF-8')})

def get_login_token(username, password):
    # Return a token if the user exists and 
    # the password matches the user's password 

    user = Account.query.filter_by(username = username).first()

    if not user:
        return None

    if check_password_hash(user.password, password):
        token = jwt.encode({'id' : str(user.id),
                            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, # expires in 60 minutes
                            current_app.config['SECRET_KEY'])
        return token

    return None

@auth.route("/logout")
def logout():
    # Since we validate our user based on the token 
    # stored in the HTTPonly secure session cookie 
    # All we do is remove it to log a user out 
    session.pop('token', None)
    return jsonify({'success': True, 'message' : "Logged out successfully."})

@auth.route("/do-register", methods=["POST"])
def do_register():
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]

    if db.session.query(Account.email).filter_by(email=email).scalar() is not None:
        return jsonify({"success": False, "reason": "Email already bound to a user."})
    elif len(username) > 25:
        return jsonify({"success": False, "reason": "Username too long."})
    elif len(first_name) > 25:
        return jsonify({"success": False, "reason": "First Name too long."})
    elif len(last_name) > 25:
        return jsonify({"success": False, "reason": "Last Name too long."})
    elif len(email) > 256 or ("@" not in email):
        return jsonify({"success": False, "reason": "Invalid email."})


    user = Account(\
        first_name=first_name,\
        last_name=last_name,\
        username=username,\
        email=email,\
        password=generate_password_hash(password, method='sha256'),\
    )

    db.session.add(user)
    db.session.commit()

    return login(username, password)
