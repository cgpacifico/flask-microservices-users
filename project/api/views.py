from flask import Blueprint, jsonify, request
from project.api.models import User
from project import db

users_blueprint = Blueprint('users', __name__)

# test helper method
def assert_required_keys(required_keys, json_data):
    # woohoo, this returns a Bool
    return required_keys <= json_data.keys()

@users_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })

@users_blueprint.route('/users', methods=['POST'])
def add_user():
    required_user_keys = {'username', 'email'}
    post_data = request.get_json()
    required_keys_present = assert_required_keys(required_user_keys, post_data)

    if not post_data or not required_keys_present:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400

    username = post_data.get('username')
    email = post_data.get('email')

    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            # db.session.add(User(username=username, email=email))
            # db.session.commit()
            response_object = {
                'status': 'success',
                'message': f'{email} was added!'
            }
        else:
            print('There is nothing in the db yet so you should never get here')

    except:
        print('no idea how we got here') 

    # wahoo, 201 Created!
    return jsonify(response_object), 201