from flask import Blueprint, session, redirect, render_template, flash, url_for
from flasksite.databases.databaseMgmt import getAllTeachers

adminTools = Blueprint('adminTools', __name__)

@adminTools.route('/grantStatus')
def grantStatus():
    if 'admin' not in session['roles']:
        return redirect(url_for('staticPages.home'))
    else:
        pass