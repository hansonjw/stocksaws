from flask import Flask

application = Flask(__name__)

@application.route("/")
def hello_world():
    return "<p>Hello, World! C'mon AWS, this has to work!</p>"