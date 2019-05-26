import uuid
import jwt
import datetime
from flask import Flask, request, session, jsonify, make_response, Blueprint, \
                render_template, flash, redirect, url_for, request, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from .models import *

auth = Blueprint("auth", __name__)

'''
Decorator to protect a view, wraps around a view function
and checks the request header for a session token, if one is
given and is valid, the view will be returned and the view function
will have access to a logged in user.
'''
def protected_view(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = session.get("token")

        if token == None:
            return jsonify({'success': False, 'message' : 'User is not authenticated. Please log in.'})

        try: 
            token_payload = jwt.decode(token, current_app.config['SECRET_KEY'])
            user = Account.query.filter_by(id = token_payload['id']).first()
        except:
            return jsonify({'success': False, 'message' : 'Something went wrong trying to authenticate you. Please try again.'})

        return f(user, *args, **kwargs)
    return decorated

@auth.route("/do-login", methods=["POST"])
def do_login():
    # Get data from the form input, check if they are valid 
    # and send login data to the login function

    username = request.form.get("email")
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
    email_exists = db.session.query(Account.email).filter_by(email=request.form["email"]).scalar() is not None

    if email_exists:
        return jsonify({"success": False, "reason": "Email already bound to a user."})

    user = Account(\
        first_name=request.form["first-name"],\
        last_name=request.form["last-name"],\
        username=request.form["username"],\
        email=request.form["email"],\
        password=generate_password_hash(request.form["password"], method='sha256'),\
    )

    # TODO: Add server-side validation (since clients can just alter the javascript to bypass client-side validation)

    db.session.add(user)
    db.session.commit()

    return login(request.form["username"], request.form["password"])
