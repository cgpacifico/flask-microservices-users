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

