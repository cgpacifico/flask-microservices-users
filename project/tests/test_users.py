import json
from project.tests.base import BaseTestCase

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
        with self.client:
            response = self.client.post(
                '/users',
                data = json.dumps(dict(
                    username='cara',
                    email='cara@snakes.com'
                )),
                content_type='application/json',
            )

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('cara@snakes.com was added!', data['message'])
            self.assertIn('success', data['status'])

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