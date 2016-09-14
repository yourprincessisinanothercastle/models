from mongoengine import StringField, Document, IntField

from models.tile import Tile
from collections import OrderedDict

class Map(Document):
    name = StringField(required=True, unique=True)
    seed = IntField()
    tilesize = IntField()
    octaves = IntField()
    steps = IntField()

    def __init__(self, name, seed, tilesize, octaves, steps, *args, **kwargs):
        Document.__init__(self, *args, **kwargs)
        self.name = name
        self.seed = seed
        self.tilesize = tilesize
        self.octaves = octaves
        self.steps = steps

        self.tilecache = OrderedDict()
        self.cachesize = 1000

    def get_tile(self, tile_x, tile_y):
        """
        get a created tile or create a new one

        :param tile_x:
        :param tile_y:
        :return:
        """
        # check if its cached
        tile = self.tilecache.get((tile_x, tile_y), False)
        if tile:
            return tile

        tile = Tile.objects.filter(name=self.name, x=tile_x, y=tile_y).first()
        if not tile:
            tile = self._make_tile(tile_x, tile_y)
        self.tilecache[(tile_x, tile_y)] = tile
        while len(self.tilecache) > self.cachesize:
            self.tilecache.popitem(last=False)
        return tile

    def _make_tile(self, tile_x, tile_y, save=False):
        t = Tile(self.name, self.seed, self.tilesize, self.octaves, self.steps, tile_x, tile_y)
        t.save()
        return t

    def get_pixel(self, x, y):
        """
        get the value for a specific pixel anywhere on the map
        creates the corresponding tile if needed

        :param x:
        :param y:
        :return:
        """
        tile_x = int(x / self.tilesize)
        tile_y = int(y / self.tilesize)

        x = x % self.tilesize
        y = y % self.tilesize

        tile = self.get_tile(tile_x, tile_y)
        return tile.get_pixel(x, y)


def save_as_pgm(name, vals, tile_x, tile_y, tilesize, steps):
    with open("%s_%s_%s.pgm" % (name, tile_x, tile_y), 'wt') as f:
        f.write('P2\n')
        f.write('%s %s\n' % (tilesize, tilesize))  # width, height
        f.write('255\n')  # max greyval
        f.write('\n'.join(str(int(val / steps * 255)) for val in vals) + '\n')
