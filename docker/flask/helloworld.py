from flask import Flask
from flask_tinyauth import login_blueprint, authorize

app = Flask(__name__)
app.register_blueprint(login_blueprint)


@app.route("/")
def hello():
    authorize('HelloWorld')

    return "Hello World!"
