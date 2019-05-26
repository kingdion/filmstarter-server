from flask import Flask

def create_app(debugMode = True):
    app = Flask(__name__)

    if debugMode:
        app.config.update(
            SQLALCHEMY_DATABASE_URI = "postgresql://postgres:isd_password@localhost:5432/filmstarter",
            SQLALCHEMY_TRACK_MODIFICATIONS = True, 
            SECRET_KEY = "Change in production",
            SESSION_COOKIE_SECURE = False,
            DEBUG = True,
        )
    else:
        app.config.update(
            SQLALCHEMY_DATABASE_URI = "postgresql://postgres:isd_password@localhost:5432/filmstarter",
            SQLALCHEMY_TRACK_MODIFICATIONS = False, 
            SECRET_KEY = "C94222125//34/rtgtrwrubwui24984524nfejsrjbf5", # randomly generated string
            SESSION_COOKIE_SECURE = True,
            DEBUG = False,
        )

    from .models import db
    db.init_app(app)

    from .authentication import auth

    app.register_blueprint(auth)

    return app