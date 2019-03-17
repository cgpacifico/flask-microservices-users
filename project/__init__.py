from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

# instantiate the app
app = Flask(__name__)

# set config
import os
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object('project.config.DevelopmentConfig')

# view the app configs, including DEBUG and TESTING
# $: docker-compose logs -f users-service
import sys
print(app.config, file=sys.stderr)

# instantiate the db
db = SQLAlchemy(app)

# user model
import datetime
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.created_at = datetime.datetime.utcnow()

@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status':'success',
        'message': 'pong!'
    })