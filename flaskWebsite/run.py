from flasksite import app

app.config['SECRET_KEY'] = 'ae98dbd984f73925c453eb1164f2b036'


if __name__ == "__main__":
    app.run(debug=True)
