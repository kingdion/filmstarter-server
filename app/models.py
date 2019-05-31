from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Account(db.Model):
    __tablename__ = 'account'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    username = db.Column(db.String(25), nullable=False, unique=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(256), nullable=False)

    projects = db.relationship(
        "Project",
        secondary="project_link",
        back_populates="accounts")

    def __init__(self, first_name, last_name, username, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = password

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns} 

class Project(db.Model):
    __tablename__ = 'project'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    production_team = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    team_code = db.Column(db.String(6), nullable=False)

    accounts = db.relationship(
        "Account",
        secondary="project_link",
        back_populates="projects")

    def __init__(self, name, production_team, description, team_code):
        self.name = name
        self.production_team = production_team
        self.description = description
        self.team_code = team_code

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns} 

class ProjectLink(db.Model):
    __tablename__ = 'project_link'

    accountId = db.Column(UUID(as_uuid=True), db.ForeignKey("account.id"), primary_key=True, default=uuid4, nullable=False)
    projectId = db.Column(UUID(as_uuid=True), db.ForeignKey("project.id"), primary_key=True, default=uuid4, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean(), default=False, nullable=False)

    def __init__(self, accountId, projectId, role, is_active):
        self.accountId = accountId
        self.projectId = projectId
        self.role = role
        self.is_active = is_active