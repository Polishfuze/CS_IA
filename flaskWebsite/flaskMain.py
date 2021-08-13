from flask import Flask, render_template, url_for

app = Flask(__name__)

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

@app.route("/")
def hello_world():
    return render_template('home.html', title='Name lmao')

@app.route("/login")
def login():
    return render_template('login.html', title='Name - login')

@app.route("/database")
def databaseDisp():
    return render_template('databaseDisp.html', students=dummyStudentData, title='Ur viewing the DB')

if __name__ == "__main__":
    app.run(debug=True)
    