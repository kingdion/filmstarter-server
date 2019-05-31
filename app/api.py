import uuid
import jwt
import datetime
import string
import random
from enum import Enum
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
    return jsonify({"success": True, "user": g.current_user.as_dict()})

@api.route("/valid-token")
@token_auth.login_required
def get_token():
    return jsonify({"success": True})

@api.route("/projects/create", methods=["POST"])
@token_auth.login_required
def create_new_project():
    project_name = request.form.get("project_name")
    team_name = request.form.get("team_name")
    description = request.form.get("description")
    
    if not project_name or not team_name or not description:
        jsonify({"success": False, "message": "Invalid request data"})

    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    proj = Project(project_name, team_name, description, code)

    db.session.add(proj)
    db.session.commit()

    link = ProjectLink(g.current_user.id, proj.id, FSRoles.director.value, False)
    db.session.add(link)
    db.session.commit()

    setActive(proj.id, True)

    return jsonify({"success": True})

def setActive(projectid, boolean_value):
    db.session.query(ProjectLink).\
       filter(ProjectLink.projectId != projectid).\
       update({"is_active": False })

    db.session.query(ProjectLink).\
       filter(ProjectLink.projectId == projectid).\
       update({"is_active": True })
    db.session.commit()


class FSRoles(Enum):
    director = "Director"
    cinematographer = "Cinematographer"
    writer = "Writer"
    actor = "Actor"
    editor = "Editor"
    unassigned = "Unassigned"
