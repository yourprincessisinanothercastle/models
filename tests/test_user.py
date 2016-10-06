import unittest
import os

from models import db

mode_before = os.environ.get('WORLDMAP_MODE', None)
os.environ['WORLDMAP_MODE'] = 'testing'
import config
from models.users.user import get_user, create_user

db_name = config.config['mongodb'].split('/')[-1]

import random


class TestUser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            db.drop_database(db_name)
        except Exception as e:
            print('couldnt delete db at startup: %s' % e)

    @classmethod
    def tearDownClass(cls):
        db.drop_database(db_name)
        if mode_before:
            os.environ['WORLDMAP_MODE'] = mode_before
        else:
            del os.environ['WORLDMAP_MODE']


    def test_user(self):
        testusername = 'testuser'
        testpassword = '321'

        self.assertFalse(get_user(testusername))

        u = create_user(testusername, testpassword)
        self.assertTrue(u.name == testusername)
        self.assertTrue(u.password_hash != testpassword)

        self.assertTrue(u.verify(testpassword))

        self.assertEquals(u.password_rounds, '200000')

