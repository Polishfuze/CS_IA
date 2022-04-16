from flask import Blueprint, render_template, session

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    if 'username' not in session:
        loggedIn = False
        roles = session['roles']
    else:
        loggedIn = True
        roles = session['roles']
    return render_template('errors/404page.html', title="Error 404", logggedIn=loggedIn, roles=roles), 404


@errors.app_errorhandler(500)
def error_500(error):
    if 'username' not in session:
        loggedIn = False
        roles = session['roles']
    else:
        loggedIn = True
        roles = session['roles']
    return render_template('errors/500page.html', title="Error 500", logggedIn=loggedIn, roles=roles), 500
