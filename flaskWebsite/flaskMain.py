from flask import Flask


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<h1>Hello, World!</h1>"

@app.route("/login")
def login():
    return "<h1>Login</h1>"


if __name__ == "__main__":
    app.run(debug=True)