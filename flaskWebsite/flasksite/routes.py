from flask import render_template, url_for, flash, redirect, session
from flasksite.forms import RegistrationForm, LoginForm
from flasksite.databaseManagement import verifyPassword, registerUser, getStudentsNormal, getAllMovement, getUserData
from itsdangerous import TimedJSONWebSignatureSerializer as TokenSerializer
from operator import itemgetter
from datetime import datetime
from flasksite import app


@app.template_filter('timestampToDate')
def pretty_date(timestamp):
    dt_object = datetime.fromtimestamp(timestamp)
    return dt_object


@app.route("/", methods=['GET', 'POST'])
def home():
    isLoggedIn = False
    if 'username' in session:
        isLoggedIn = True
    return render_template('home.html', title='Name lmao', loggedIn=isLoggedIn)


# Needed for debugging
@app.route("/lipsum", methods=['GET', 'POST'])
def lipsum():
    return render_template('lipsum.html', title='lipsum')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'username' in session:
        print(session['username'])
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        if verifyPassword(form.username.data, form.password.data):
            flash('You have been loggen in!', 'success')
            session['username'] = form.username.data
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful, please check your username and password', 'danger')
    return render_template('login.html', title='Name - login', form=form)


@app.route("/footer")
def footer():
    return render_template('footerReplacement.html', title='Name - login')


@app.route("/database", methods=['GET', 'POST'])
def databaseDisp():
    if 'username' not in session:
        flash('You must be logged in to view that section!', 'danger')
        return redirect(url_for('login'))
    data = getAllMovement()
    sortedStudents = sorted(data, key=itemgetter('MovementID'), reverse=True)

    return render_template('databaseDisp.html', students=sortedStudents, title='Ur viewing the DB')


@app.route("/students", methods=['GET', 'POST'])
def students():
    if 'username' not in session:
        flash('You must be logged in to view that section!', 'danger')
        return redirect(url_for('login'))
    return render_template('students.html', students=getStudentsNormal(), title='Ur viewing the DB')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        registerUser(form.username.data, form.email.data, form.password.data)
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Name - register', form=form)


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    if 'username' in session:
        return redirect(url_for('home'))
    s = TokenSerializer(app.config['SECRET_KEY'])
    username = ''
    try:
        username = s.loads(token)
    except:
        flash('That token is invalid or expired!', 'warning')
        return redirect(url_for('home'))
    userData = getUserData(username)
