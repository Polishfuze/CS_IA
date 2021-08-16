from flask import Flask

app = Flask(__name__)

SECRET_KEY = 'ae98dbd984f73925c453eb1164f2b036'

from flasksite.users.routes import users
from flasksite.databases.routes import databases
from flasksite.staticPages.routes import staticPages
app.register_blueprint(users)
app.register_blueprint(databases)
app.register_blueprint(staticPages)
