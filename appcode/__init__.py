import os
from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    application = Flask(__name__, instance_relative_config=True)
    application.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(application.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        application.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        application.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(application.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @application.route('/')
    def hello():
        return '<p>Hello, AWS!</p><a href="/today">today link</a>'

    import appcode.routes.routes as routes
    application.register_blueprint(routes.bp)
   
    return application

application = create_app()