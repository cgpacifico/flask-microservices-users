import json
from project import db
from project.tests.base import BaseTestCase
from project.api.models import User

def db_add_user_helper(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user

class TestUserService(BaseTestCase):
    "Tests for the Users Service"

    def test_ping_route(self):
        """Ensure the /ping route responds correctly"""
        response = self.client.get('/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])
    
    def test_nonexistant_route(self):
        """Ensure a nonexistant route responds correctly"""
        response = self.client.get('/not-a-route')
        self.assertEqual(response.status_code, 404)
        # print('reponse', response) YIELDS <TestResponse streamed [404 NOT FOUND]>

    def test_create_user(self):
        """Ensure a new user is added to the database with proper response"""
        username = 'cara'
        email = 'cara@snakes.com'
        with self.client:
            response = self.client.post(
                '/users',
                data = json.dumps(dict(
                    username=username,
                    email=email
                )),
                content_type='application/json',
            )

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('cara@snakes.com was added!', data['message'])
            self.assertIn('success', data['status'])
            user = User.query.filter_by(email=email).first()
            self.assertFalse(user is None)

    def test_create_user_without_payload(self):
        """Ensure error is thrown if the JSON object is empty"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict()),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400) 
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])               

    def test_create_user_without_username(self):
        """Ensure error is thrown if the JSON object does not have a username"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict(email='no_username@sonlyemail.com')),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_create_user_without_email(self):
        """Ensure error is thrown if the JSON object does not have an email"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict(username='only-name-no-email')),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])
    
    def test_create_user_duplicate_user(self):
        """Ensure error is thrown if the email already exists"""
        with self.client:
            self.client.post(
                '/users',
                data=json.dumps(dict(
                    username='existing_user',
                    email='existing_user@test.com'
                )),
                content_type='application/json',
            )
            response = self.client.post(
                '/users',
                data=json.dumps(dict(
                    username='different_username',
                    email='existing_user@test.com'
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. That email already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_read_user(self):
        """Ensure getting a single user behaves correctly."""
        username = 'single_user'
        email = 'get@one_user.com'
        # this User method forms a user object
        # user = User(username=username, email=email)
        # # then adds it
        # db.session.add(user)
        # # then saves it
        # db.session.commit()

        # use my helper instead
        user = db_add_user_helper(username=username, email=email)

        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue('created_at' in data['data'])
            self.assertIn(username, data['data']['username'])
            self.assertIn(email, data['data']['email'])
            self.assertIn('success', data['status'])

    def test_read_user_no_id(self):
        """Ensure error is thrown if a user id is invalid"""
        with self.client:
            response = self.client.get('/users/not-an-id')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_read_user_nonexistant_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            # blew out that number, just in case there is TONS of test data, someday ;)
            # cannot make it TOO big, or:
            # sqlalchemy.exc.DataError: (psycopg2.DataError) value "99999999999999999" is out of range for type integer
            response = self.client.get('/users/99999999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_read_all_users(self):
        username1 = 'andrew'
        username2 = 'zoe'
        email1 = 'andrew@email1.com'
        email2 = 'zoe@email2.com'

        """Ensure get all users behaves correctly."""
        db_add_user_helper(username1, email1)
        db_add_user_helper(username2, email2)
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertTrue('created_at' in data['data']['users'][0])
            self.assertTrue('created_at' in data['data']['users'][1])
            self.assertIn(username1, data['data']['users'][0]['username'])
            self.assertIn(
                email1, data['data']['users'][0]['email'])
            self.assertIn(username2, data['data']['users'][1]['username'])
            self.assertIn(
                email2, data['data']['users'][1]['email'])
            self.assertIn('success', data['status'])


