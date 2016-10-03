import unittest
import os

from worldmap import db

mode_before = os.environ.get('WORLDMAP_MODE', None)
os.environ['WORLDMAP_MODE'] = 'testing'
import config
from worldmap.world import World

db_name = config.config['mongodb'].split('/')[-1]

import random


class TestWorldmap(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            db.drop_database(db_name)
        except Exception as e:
            print('couldnt delete db at startup: %s' % e)

        # -25432, 63113 with seed 34137
        # 45766, -58087 with seed -14045 # get neighbors fail


        cls.seed = random.randint(-90000, 90000)
        cls.w = World('testworld', cls.seed, 64, 2).save()
        cls.rand_x = random.randint(-90000, 90000)
        cls.rand_y = random.randint(-90000, 90000)
        cls.v = cls.w.get_voronoi(cls.rand_x, cls.rand_y)

        print('testing on %s, %s with seed %s' % (cls.rand_x, cls.rand_y, cls.seed))

    @classmethod
    def tearDownClass(cls):
        db.drop_database(db_name)
        if mode_before:
            os.environ['WORLDMAP_MODE'] = mode_before
        else:
            del os.environ['WORLDMAP_MODE']

    def test_get_voronoi(self):
        self.assertIsNotNone(self.v)

    def test_vor_coord(self):
        c = self.v.voronoi_coord
        x = c[0]
        y = c[1]

        # our values are at least 10 times as big as on the tilemap, because we are scaling up
        self.assertGreaterEqual(abs(x), abs(self.rand_x * 10))
        self.assertGreaterEqual(abs(y), abs(self.rand_y * 10))

    def test_vor_get_geighbors(self):
        n = self.v.neighbors
        self.assertGreaterEqual(len(n), 2)

    def test_get_shape(self):
        self.assertGreaterEqual(len(self.v.shape), 3)  # at least 3 corners

    def test_get_shape2(self):
        print('\n\n')
        print(self.v.shape)
        print('\n\n')
        # print(self.v._get_shape1(self.rand_x, self.rand_y))
        # print('\n\n')
        print(measure_time(self.v._get_shape2, self.rand_x, self.rand_y))
        print('\n\n')
        print(measure_time(self.v._get_shape3, self.rand_x, self.rand_y))
        print('\n\n')
        print(measure_time(self.v._get_shape4, self.rand_x, self.rand_y))
        print('\n\n')
        print(measure_time(self.v._get_shape5, self.rand_x, self.rand_y))
        print('\n\n')
        print('%s/%s' % (len(self.v.shape), len(self.v._get_shape2(self.rand_x, self.rand_y))))
        # self.assertTrue(self.v.shape == self.v._get_shape2(self.rand_x, self.rand_y))  # at least 3 corners

    def test_shapesize(self):
        self.assertGreater(self.v.shape_size, 0)

    def test_biome(self):
        self.assertTrue(self.v.biome is not None)

    def test_points_in_biome(self):
        print('biome fields: %s (%s)' % (len(self.v.points_in_biome), self.v.biome))
        self.assertGreater(len(self.v.points_in_biome), 0)

    def test_neighbors_shapes(self):
        """
        neighbors shapes should have two points of the shape in common
        :return:
        """
        n = self.v.neighbors[0]
        intersect = set.intersection(set(self.v.shape), set(n.shape))
        self.assertTrue(len(intersect), 2)


def measure_time(function, *args, **kwargs):
    import time
    before = time.time()
    r = function(*args, **kwargs)
    after = time.time()
    print('took %ss' % (after - before))
    return r
