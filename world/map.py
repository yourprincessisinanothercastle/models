"""
create map with perlin noise

map is initialized with name and seed,
the map tiles can be created then with make_tile(coord_x, coord_y)

saves the tile to name_x_y.pgm


needs a "pip install noise"
"""


from noise.perlin import SimplexNoise

import random

from math import floor

import argparse


class Map:
    def __init__(self, name, seed=None, tilesize=256, octaves=8, granularity=256, savetiles=False):
        self.octaves = octaves
        self.freq = 16.0 * self.octaves  # size of the blobs
        self.seed = seed
        self.tilesize = tilesize
        self.name = name
        self.r = random.Random(self.seed)
        self.granularity = granularity

        self.tiles = {}  # store tiles at runtime
        self.savetiles = savetiles

    def get_tile(self, tile_x, tile_y):
        """
        get a created tile or create a new one

        :param tile_x:
        :param tile_y:
        :return:
        """
        tile = self.tiles.get((tile_x, tile_y), False)
        if not tile:
            self.tiles[(tile_x, tile_y)] = self._make_tile(tile_x, tile_y, save=self.savetiles)
        return self.tiles[(tile_x, tile_y)]

    def _make_tile(self, tile_x, tile_y, save=False):
        """
        generate a tile

        :param tile_x:
        :param tile_y:
        :param save:
        :return:
        """
        n = SimplexNoise()

        # shuffle the permutation list
        perm_list = list(n.permutation)
        self.r.shuffle(perm_list)
        n.permutation = tuple(perm_list)

        vals = []
        for y in range(self.tilesize):
            for x in range(self.tilesize):
                value = n.noise2((x + self.tilesize * tile_x) / self.freq, (y + self.tilesize * tile_y) / self.freq)
                #print('val: %s' % value)
                vals.append(int(value * (self.granularity/2 ) + (self.granularity / 2 )))  # scale up & shift negative values above zero and append
        #print(self.name + ' '.join([str(x) for x in vals if x >= 4]))
        if save:
            save_as_pgm(self.name, vals, tile_x, tile_y, self.tilesize, self.granularity)
        return vals

    def get_pixel(self, x, y):
        """
        get the value for a specific pixel anywhere on the map
        creates the corresponding tile if needed

        :param x:
        :param y:
        :return:
        """
        tile_x = int(x/self.tilesize)
        tile_y = int(y/self.tilesize)

        x = x % self.tilesize
        y = y % self.tilesize

        values = self.get_tile(tile_x, tile_y)
        return values[y * self.tilesize + x]




def save_as_pgm(name, vals, tile_x, tile_y, tilesize, granularity):
    with open("%s_%s_%s.pgm" % (name, tile_x, tile_y), 'wt') as f:
        f.write('P2\n')
        f.write('%s %s\n' % (tilesize, tilesize))  # width, height
        f.write('255\n')  # max greyval
        f.write('\n'.join(str(int(val / granularity * 255)) for val in vals) + '\n')



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("seed")
    parser.add_argument("tile_x", type=int)
    parser.add_argument("tile_y", type=int)
    args = parser.parse_args()

    map = Map(args.name, args.seed)

    map.get_tile(args.tile_x, args.tile_y)
