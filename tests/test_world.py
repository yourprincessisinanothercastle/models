import unittest
import os

from models import db

mode_before = os.environ.get('WORLDMAP_MODE', None)
os.environ['WORLDMAP_MODE'] = 'testing'
import config
from models.world import World

db_name = config.config['mongodb'].split('/')[-1]


import random

class TestWorldmap(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            db.drop_database(db_name)
        except Exception as e:
            print('couldnt delete db at startup: %s' % e)

        cls.w = World('testworld', 321, 64, 2).save()
        cls.rand_x = random.randint(-90000, 90000)
        cls.rand_y = random.randint(-90000, 90000)

        print('testing on %s, %s' % (cls.rand_x, cls.rand_y))

    @classmethod
    def tearDownClass(cls):
        db.drop_database(db_name)
        if mode_before:
            os.environ['WORLDMAP_MODE'] = mode_before
        else:
            del os.environ['WORLDMAP_MODE']

    def test_worldcreation(self):
        self.assertTrue(self.w is not None)

    def test_temp(self):
        t = self.w.get_temperature(self.rand_x, self.rand_y)
        self.assertTrue(t >= 0)

    def test_height(self):
        t = self.w.get_height(self.rand_x, self.rand_y)
        self.assertTrue(t >= 0)

    def test_biome(self):
        t = self.w.get_biome(self.rand_x, self.rand_y)
        self.assertTrue(type(t) == str)
        self.assertTrue(len(t) > 0)





if __name__ == '__main__':
    unittest.main()
