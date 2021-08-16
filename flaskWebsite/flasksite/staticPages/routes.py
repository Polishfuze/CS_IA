from flask import Blueprint, session, render_template, url_for

staticPages = Blueprint('staticPages', __name__)


@staticPages.route("/", methods=['GET', 'POST'])
def home():
    isLoggedIn = False
    if 'username' in session:
        isLoggedIn = True
    return render_template('home.html', title='Name lmao', loggedIn=isLoggedIn)


# Needed for debugging
@staticPages.route("/lipsum", methods=['GET', 'POST'])
def lipsum():
    return render_template('lipsum.html', title='lipsum')


@staticPages.route("/footer")
def footer():
    return render_template('footerReplacement.html', title='Name - login')
