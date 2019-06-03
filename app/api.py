import uuid
import jwt
import datetime
import string
import json
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

    setActive(proj.id)

    return jsonify({"success": True})

@api.route("/projects/get", methods=["GET"])
@token_auth.login_required
def get_all_projects():
    query = db.session.query(Project).filter(ProjectLink.accountId == g.current_user.id).all()

    proj = [project.as_dict() for project in query]
    applicable_projects = []

    for project in proj:
        link = db.session.query(ProjectLink).filter((ProjectLink.accountId == g.current_user.id) & (ProjectLink.projectId == project["id"])).first()

        if link:
            project["is_active"] = link.is_active
            project["role"] = link.role

            applicable_projects.append(project)

    return jsonify({"success": True,  "projects": applicable_projects})

@api.route("/projects/get/current", methods=["GET"])
@token_auth.login_required
def get_current_project():
    query = db.session.query(Project).filter(ProjectLink.accountId == g.current_user.id).all()

    proj = [project.as_dict() for project in query]
    applicable_projects = []

    for project in proj:
        link = db.session.query(ProjectLink).filter((ProjectLink.accountId == g.current_user.id) & (ProjectLink.projectId == project["id"])).first()

        if link and link.is_active == True:
            project["is_active"] = link.is_active
            project["role"] = link.role

            applicable_projects.append(project)

    return jsonify({"success": True,  "projects": applicable_projects})
    

@api.route("/projects/team/users", methods=["GET"])
@token_auth.login_required
def get_team_users():
    query = db.session.query(Project).filter(ProjectLink.accountId == g.current_user.id).all()

    proj = [project.as_dict() for project in query]
    applicable_projects = []

    for project in proj:
        link = db.session.query(ProjectLink).filter((ProjectLink.accountId == g.current_user.id) & (ProjectLink.projectId == project["id"])).first()

        if link and link.is_active == True:
            project["is_active"] = link.is_active
            project["role"] = link.role

            applicable_projects.append(project)

    users_query = db.session.query(ProjectLink).filter((ProjectLink.projectId == applicable_projects[0]["id"])).all()
    users = [linky.as_dict() for linky in users_query]

    return jsonify({"success": True,  "users": users})

@api.route("/projects/select", methods=["POST"])
@token_auth.login_required
def select_project():
    project_id = request.form.get("project_id")
    
    if not project_id:
        return jsonify({"success": False, "message": "Invalid request data"})

    setActive(project_id)

    return jsonify({"success": True})

@api.route("/projects/add", methods=["POST"])
@token_auth.login_required
def add_to_project():
    project_id = uuid.UUID(request.form.get("project_id"))
    user_id = uuid.UUID(request.form.get("user_id"))
    role = request.form.get("role")

    if not project_id or not user_id:
        return jsonify({"success": False, "message": "Invalid request data"})

    project = db.session.query(Project).filter(ProjectLink.projectId == project_id).first()

    if not project:
        return jsonify({"success": False, "message": "This project doesn't exist"}) 

    exists = db.session.query(Project).filter((ProjectLink.projectId == project_id) & (ProjectLink.accountId == user_id)).first()
    if exists:
        return jsonify({"success": False, "message": "This project link already exist"}) 

    link = ProjectLink(user_id, project.id, role, False)
    db.session.add(link)
    db.session.commit()
    
    return jsonify({"success": True})

def setActive(projectid):
    try:
        db.session.query(ProjectLink).\
            filter((ProjectLink.projectId != projectid) & (ProjectLink.accountId == g.current_user.id)).\
            update({"is_active": False })

        db.session.query(ProjectLink).\
            filter((ProjectLink.projectId == projectid) & (ProjectLink.accountId == g.current_user.id)).\
            update({"is_active": True })
    except:
       return jsonify({"success": False, "message": "Something went wrong..."}) 

    db.session.commit()


class FSRoles(Enum):
    director = "Director"
    cinematographer = "Cinematographer"
    writer = "Writer"
    actor = "Actor"
    editor = "Editor"
    unassigned = "Unassigned"
