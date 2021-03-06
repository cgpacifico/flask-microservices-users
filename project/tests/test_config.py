import unittest
import os
# from secrets import KEY
from flask import current_app
from flask_testing import TestCase
from project import create_app

app = create_app()


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        # self.assertFalse(app.config['SECRET_KEY'] is None)
        # self.assertTrue(app.config['SECRET_KEY'] == 'my_precious')
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] ==
            # FIX - get the DB's URL from the environment
            os.environ.get('DATABASE_URL')
        )

class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        # self.assertFalse(app.config['SECRET_KEY'] is None)
        # self.assertTrue(app.config['SECRET_KEY'] == KEY)
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(app.config['TESTING'])
        self.assertFalse(app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] ==
            os.environ.get('DATABASE_TEST_URL')
        )

class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        # self.assertFalse(app.config['SECRET_KEY'] is None)
        # self.assertTrue(app.config['SECRET_KEY'] == KEY)
        self.assertFalse(app.config['DEBUG'])
        self.assertFalse(app.config['TESTING'])
