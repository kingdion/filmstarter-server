import datetime
import string
import random
from app import create_app
from app.models import *
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
app = create_app()
with app.app_context():
        db.drop_all()
        db.create_all()

        user1 = Account("John", "Doe", "TestUser01", "testuser01@gmail.com", generate_password_hash("TestUser01", method='sha256'))
        user2 = Account("Jane", "Doe", "TestUser02", "testuser02@gmail.com", generate_password_hash("TestUser02", method='sha256'))
        user3 = Account("Writer", "Doe", "TestUser03", "testuser03@gmail.com", generate_password_hash("TestUser03", method='sha256'))
        user4 = Account("Cinematographer", "Doe", "TestUser04", "testuser04@gmail.com", generate_password_hash("TestUser04", method='sha256'))

        project1 = Project("Harry Potter", "Warner Brothers", "A movie about wizards", ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)))
        project2 = Project("Star Wars", "Lucasfilms", "A movie about wizards with swords", ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)))
        project3 = Project("The Avengers", "Marvel", "A movie about heroes n stuff", ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)))
        project4 = Project("The Avengers: Endgame", "Marvel", "A movie about heroes n stuff and thanos", ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)))

        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        db.session.add(user4)
        db.session.add(project1)
        db.session.add(project2)
        db.session.add(project3)
        db.session.add(project4)

        db.session.commit()

        project_link = ProjectLink(user1.id, project1.id, "Director", True)
        project_link2 = ProjectLink(user2.id, project1.id, "Actor", True)
        project_link3 = ProjectLink(user3.id, project1.id, "Writer", True)
        project_link4 = ProjectLink(user4.id, project1.id, "Cinematographer", True)

        project_link5 = ProjectLink(user1.id, project2.id, "Writer", False)
        project_link6 = ProjectLink(user2.id, project2.id, "Director", True)

        db.session.add(project_link)
        db.session.add(project_link2)
        db.session.add(project_link3)
        db.session.add(project_link4)
        db.session.add(project_link5)
        db.session.add(project_link6)

        db.session.commit()