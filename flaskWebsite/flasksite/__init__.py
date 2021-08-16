from flasksite.databases.routes import databases
from flasksite.staticPages.routes import staticPages
from flasksite.users.routes import users
from flask import Flask
from flasksite.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(users)
    app.register_blueprint(databases)
    app.register_blueprint(staticPages)

    return app