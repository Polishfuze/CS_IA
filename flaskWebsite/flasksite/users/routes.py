from flask import Blueprint, session, url_for, redirect, render_template, flash, current_app
from flasksite.users.databaseMgmt import verifyPassword, registerUser, getUserData
from flasksite.users.forms import LoginForm, RegistrationForm
from itsdangerous import TimedJSONWebSignatureSerializer as TokenSerializer


users = Blueprint('users', __name__)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if 'username' in session:
        print(session['username'])
        return redirect(url_for('staticPages.home'))
    form = LoginForm()
    if form.validate_on_submit():
        pwdCheck = verifyPassword(form.username.data, form.password.data)
        if pwdCheck[0]:
            flash('You have been loggen in!', 'success')
            session['username'] = form.username.data
            session['roles'] = pwdCheck[1]
            print(session['roles'])
            return redirect(url_for('staticPages.home'))
        else:
            flash('Login unsuccessful, please check your username and password', 'danger')
    return render_template('login.html', title='Name - login', logggedIn=False, roles=[], form=form)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('staticPages.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        registerUser(form.username.data, form.email.data, form.password.data)
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('staticPages.home'))
    return render_template('register.html', title='Name - register', logggedIn=False, roles=[], form=form)


@users.route("/logout", methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('staticPages.home'))


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    if 'username' in session:
        return redirect(url_for('staticPages.home'))
    s = TokenSerializer(current_app.config['SECRET_KEY'])
    username = ''
    try:
        username = s.loads(token)
    except:
        flash('That token is invalid or expired!', 'warning')
        return redirect(url_for('staticPages.home'))
    userData = getUserData(username)
