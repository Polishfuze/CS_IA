from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404page.html'), 404


@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500page.html'), 500
