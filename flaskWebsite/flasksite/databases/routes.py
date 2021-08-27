from flask import Blueprint, session, redirect, render_template, flash, url_for
from flasksite.databases.databaseMgmt import getAllMovement, getStudentsNormal
from operator import itemgetter
from datetime import datetime

databases = Blueprint('databases', __name__)


@databases.app_template_filter('timestampToDate')
def pretty_date(timestamp):
    dt_object = datetime.fromtimestamp(timestamp)
    return dt_object


@databases.route("/database", methods=['GET', 'POST'])
def databaseDisp():
    if 'username' not in session:
        flash('You must be logged in to view that section!', 'danger')
        return redirect(url_for('users.login'))
    else:
        loggedIn = True
        roles = session['roles']
    data = getAllMovement()
    sortedStudents = sorted(data, key=itemgetter('MovementID'), reverse=True)

    return render_template('databaseDisp.html', students=sortedStudents, title='Ur viewing the DB but detailed', logggedIn=loggedIn, roles=roles)


@databases.route("/students", methods=['GET', 'POST'])
def students():
    if 'username' not in session:
        flash('You must be logged in to view that section!', 'danger')
        return redirect(url_for('users.login'))
    else:
        loggedIn = True
        roles = session['roles']
    return render_template('students.html', students=getStudentsNormal(), title='Ur viewing the DB', logggedIn=loggedIn, roles=roles)
