import json
from project.tests.base import BaseTestCase
from project.api.models import User

class TestUserService(BaseTestCase):
    "Tests for the Users Service"

    def test_ping_route(self):
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

    def test_create_user(self):
        # this could maybe be two separate tests but... meh
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
            # NOW this test really proves the user is in the db!
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
        pass
