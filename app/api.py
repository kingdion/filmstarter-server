import uuid
import jwt
import datetime
from flask import Flask, request, session, jsonify, make_response, Blueprint, \
                render_template, flash, redirect, url_for, request, jsonify, current_app, g
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from .models import *
from .authentication import token_auth

api = Blueprint("api", __name__)

@api.route("/get-user")
@token_auth.login_required
def get_user():
    return jsonify(g.current_user.as_dict())