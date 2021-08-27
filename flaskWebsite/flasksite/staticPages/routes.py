from flask import Blueprint, session, render_template, url_for

staticPages = Blueprint('staticPages', __name__)


@staticPages.route("/", methods=['GET', 'POST'])
def home():
    if 'username' in session:
        loggedIn = True
        roles = session['roles']
        username = session['username']
    else:
        roles = []
        loggedIn = False
        username = ""
    return render_template('home.html', title='Name lmao', logggedIn=loggedIn, roles=roles, username=username)


# Needed for debugging
@staticPages.route("/lipsum", methods=['GET', 'POST'])
def lipsum():
    if 'username' in session:
        loggedIn = True
        roles = session['roles']
    else:
        roles = []
        loggedIn = False
    return render_template('lipsum.html', title='lipsum', logggedIn=loggedIn, roles=roles)


@staticPages.route("/footer")
def footer():
    if 'username' in session:
        loggedIn = True
        roles = session['roles']
    else:
        roles = []
        loggedIn = False
    return render_template('footerReplacement.html', title='Name - login', logggedIn=loggedIn, roles=roles)
