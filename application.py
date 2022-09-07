from flask import Flask
application = Flask(__name__)

# application instead of app, convention with AWS
@application.route('/')
def hello_world():
   return "Hello, World! way to go AWS, this is working!?"

# This was included for the tutorial of lightsail
# if __name__ == "__main__":
#    app.run(host='0.0.0.0', port=5000)