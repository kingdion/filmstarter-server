import os
import datetime
from flask import render_template, flash, redirect, url_for, request, jsonify
from app import create_app
from app.models import db

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
