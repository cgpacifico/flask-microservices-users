from flask import Flask, jsonify

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

@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status':'success',
        'message': 'pong!'
    })