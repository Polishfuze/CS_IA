from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from databaseManagement import verifyPassword, registerUser

app = Flask(__name__)

app.config['SECRET_KEY']='ae98dbd984f73925c453eb1164f2b036'

dummyStudentData = [
    {
        'name':'Michal',
        'time':'12:37',
        'isinSchool':'False'
    },
    {
        'name':'Chris',
        'time':'12:38',
        'isinSchool':'True'
    }
]

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('home.html', title='Name lmao')


# Needed for debugging
@app.route("/lipsum", methods=['GET', 'POST'])
def lipsum():
    return render_template('lipsum.html', title='lipsum')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if verifyPassword(form.username.data, form.password.data):
            flash('You have been loggen in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful, please check your username and password', 'danger')
    return render_template('login.html', title='Name - login', form=form)

@app.route("/footer")
def footer():
    return render_template('footerReplacement.html', title='Name - login')

@app.route("/database", methods=['GET', 'POST'])
def databaseDisp():
    return render_template('databaseDisp.html', students=dummyStudentData, title='Ur viewing the DB')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Name - register', form=form)

if __name__ == "__main__":
    app.run(debug=True)
    

    