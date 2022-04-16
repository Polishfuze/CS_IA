from flask import Blueprint, session, redirect, render_template, flash, url_for, request
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
    sortedStudents = sorted(data, key=itemgetter('Timestamp'), reverse=True)
    return render_template('databaseDisp.html', students=sortedStudents, title='Detailed database view', logggedIn=loggedIn, roles=roles)



@databases.route("/students", methods=['GET', 'POST'])
def students():
    if 'username' not in session:
        flash('You must be logged in to view that section!', 'danger')
        return redirect(url_for('users.login'))
    else:
        loggedIn = True
        roles = session['roles']
    return render_template('students.html', students=getStudentsNormal(), title='Student status view', logggedIn=loggedIn, roles=roles)


@databases.route("/addstudents", methods=['GET', 'POST'])
def addStudents():
    form = AddStudentForm(request.form)
    form.teacherName.choices=getAllTeachers()
    # print('a')
    if 'teacher' not in session['roles']:
        flash('You must be a teacher to view that section!', 'danger')
        return redirect(url_for('users.login'))
    else:
        loggedIn = True
        roles = session['roles']
    # print('b')
    valid = form.validate()
    print(form.errors)
    if valid:
        print('e')
        addStudentsToProg(form.studentName.data, form.teacherName.data)
        flash(f'Account created for {form.studentName.data}!', 'success')
    return render_template('addStudents.html', students=getStudentsNormal(), title='Add students', logggedIn=loggedIn, roles=roles, form=form)
