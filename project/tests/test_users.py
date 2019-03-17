import json
from project.tests.base import BaseTestCase
from project.api.models import User

class TestUserService(BaseTestCase):
    "Tests for the Users Service"

    def test_users(self):
        """Ensure the /ping route responds correctly"""
        # self.client.get ? nifty utility method is nifty!
        response = self.client.get('/ping')
        data = json.loads(response.data.decode())
        # print('hey look I can print a message', data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])
    
    def test_nonexistant_route(self):
        """Ensure a nonexistant route responds correctly"""
        response = self.client.get('/not-a-route')
        self.assertEqual(response.status_code, 404)
        # print('reponse', response) YIELDS <TestResponse streamed [404 NOT FOUND]>

    def test_add_user(self):
        """Ensure a new user can be added to the database"""
        # booo nothing about this test proves this information made it to the database
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
            # this maybe is all I need
            user = User.query.filter_by(email=email).first()
            self.assertFalse(user is None)
            
            # just proving that's a valid check
            nope = User.query.filter_by(email='wat').first()
            self.assertFalse(nope is None) # self.assertFalse(nope is None)
                # AssertionError: True is not false

            # object
            print(user) # <project.api.models.User object at 0x7feab1bc2ba8>
            
            # getting actual data
            print('I have the user', user.__dict__) # {'_sa_instance_state': <sqlalchemy.orm.state.InstanceState object at 0x7feab1bc2be0>, 'active': False, 'username': 'cara', 'created_at': datetime.datetime(2019, 3, 17, 20, 42, 46, 835495), 'email': 'cara@snakes.com', 'id': 1}


    def test_add_user_without_payload(self):
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

    def test_add_user_without_username(self):
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

    def test_add_user_without_email(self):
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
    
    def test_add_user_duplicate_user(self):
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