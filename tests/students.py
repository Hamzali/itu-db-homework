import unittest
import os
import json
from server import app, db

class BucketlistTestCase(unittest.TestCase):
    """This class represents the bucketlist test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.bucketlist = {'name': 'Go to Borabora for vacay'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_get_all_students(self):
        """Test API can list all students (POST request)"""
        res = self.client().get('/students')
        self.assertEqual(res.status_code, 200)
        
