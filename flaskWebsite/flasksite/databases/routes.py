from flask import Blueprint, session, redirect, render_template, flash, url_for
from flasksite.databases.databaseMgmt import getAllMovement, getStudentsNormal, addStudentsToProg, getAllTeachers
from flasksite.databases.forms import AddStudentForm
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


@databases.route("/addstudents", methods=['GET', 'POST'])
def addStudents():
    print('a')
    if 'teacher' not in session['roles']:
        flash('You must be a teacher to view that section!', 'danger')
        return redirect(url_for('users.login'))
    else:
        loggedIn = True
        roles = session['roles']
    print('b')
    form = AddStudentForm()
    form.teacherName.choices=getAllTeachers()
    return render_template('addStudents.html', students=getStudentsNormal(), title='Ur viewing the DB', logggedIn=loggedIn, roles=roles, form=form)
