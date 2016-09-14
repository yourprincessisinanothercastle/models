from mongoengine import StringField, Document, IntField, ReferenceField, ListField
from noise.perlin import SimplexNoise

import random


class Tile(Document):
    tilesize = IntField()
    data = ListField(IntField(), default=list)
    name = StringField()
    seed = IntField()
    octaves = IntField()
    steps = IntField()
    x = IntField()
    y = IntField()

    meta = {
        'indexes': [
            {
                'fields': ['-data', 'name', 'x', 'y'],
                'unique': False,
                'sparse': True,
                'types': False},
        ],
    }

    def __init__(self, name, seed, tilesize, octaves, steps, x, y, *args, **kwargs):
        """
        generate a tile

        :param tile_x:
        :param tile_y:
        :param save:
        :return:
        """
        Document.__init__(self, *args, **kwargs)

        self.name = name
        self.seed = seed
        self.tilesize = tilesize
        self.octaves = octaves
        self.steps = steps

        self.r = random.Random(self.seed)

        self.freq = 16.0 * self.octaves  # size of the blobs

        self.x = x
        self.y = y

        if not self.data:
            #print('creating new tile for %s: %s, %s' % (name, x, y))
            self.generate()

    def generate(self):
        tile_x = self.x
        tile_y = self.y

        n = SimplexNoise()

        # shuffle the permutation list
        perm_list = list(n.permutation)
        self.r.shuffle(perm_list)
        n.permutation = tuple(perm_list)

        vals = []
        for y in range(self.tilesize):
            for x in range(self.tilesize):
                value = n.noise2((x + self.tilesize * tile_x) / self.freq, (y + self.tilesize * tile_y) / self.freq)
                # print('val: %s' % value)
                vals.append(int(value * (self.steps / 2) + (
                    self.steps / 2)))  # scale up & shift negative values above zero and append
        # print(self.name + ' '.join([str(x) for x in vals if x >= 4]))
        self.data = vals

    def get_pixel(self, x, y):
        return self.data[y * self.tilesize + x]
