import uuid
import jwt
import datetime
from flask import Flask, request, session, jsonify, make_response, Blueprint, \
                render_template, flash, redirect, url_for, request, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from .models import *
from .authentication import protected_view

api = Blueprint("api", __name__)

@api.route("/validate-token")
@protected_view
def validate_token(user):
    return jsonify({'success': True, 'user' : user.__dict__})