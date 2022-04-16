from flask import Flask
from flasksite.databases.routes import databases
from flasksite.staticPages.routes import staticPages
from flasksite.users.routes import users
from flasksite.errors.handlers import errors
# from flasksite.adminTools.routes import adminTools  
from flasksite.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.register_blueprint(users)
    app.register_blueprint(errors)
    app.register_blueprint(databases)
    app.register_blueprint(staticPages)
    # app.register_blueprint(adminTools)

    return app