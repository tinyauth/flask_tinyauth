from flask import Flask
from flask_tinyauth import login_blueprint, authorize_or_401, authorize_or_login


app = Flask(__name__)
app.register_blueprint(login_blueprint)

app.config['TINYAUTH_SERVICE'] = 'helloworld'
app.config['TINYAUTH_REGION'] = 'eu-west-1'
app.config['TINYAUTH_PARTITION'] = 'primary'
app.config['TINYAUTH_ENDPOINT'] = 'http://tinyauth:5000/'
app.config['TINYAUTH_ACCESS_KEY_ID'] = 'gatekeeper'
app.config['TINYAUTH_SECRET_ACCESS_KEY'] = 'keymaster'


@app.route("/api/")
def hello_api():
    authorize_or_401('HelloWorld')

    return '{"message":"Hello World!"}'


@app.route("/")
def hello():
    authorize_or_login('HelloWorld')

    return "Hello World!"
