import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

# view the app configs, including DEBUG and TESTING
# $: docker-compose logs -f users-service
# import sys
# print(app.config, file=sys.stderr)

# instantiate the db
# you no longer pass it the app - looks like you do that in a separate step, later
# db = SQLAlchemy(app)
db = SQLAlchemy()


def create_app():
    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object('project.config.DevelopmentConfig')
    # app.config.from_object(app_settings)

    # set up extensions (SQLAlchemy method)
    db.init_app(app)

    # register blueprints
    from project.api.views import users_blueprint
    app.register_blueprint(users_blueprint)

    return app