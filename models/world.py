from mongoengine import StringField, Document, IntField, ReferenceField
from .constants import COLORS, BIOMES

from models.map import Map


class World(Document):
    name = StringField(required=True, unique=True)
    seed = IntField()
    tilesize = IntField()
    octaves = IntField()

    heightmap = ReferenceField(Map)
    tempmap = ReferenceField(Map)

    def __init__(self, name, seed, tilesize, octaves, *args, **kwargs):
        Document.__init__(self, *args, **kwargs)

        self.name = name
        self.seed = seed
        self.tilesize = tilesize
        self.octaves = octaves

        if not self.heightmap and not self.tempmap:
            self.create_maps()

    def create_maps(self):
        self.heightmap = Map(self.name + "_height", seed=self.seed, tilesize=self.tilesize, octaves=self.octaves,
                             steps=5).save()
        self.tempmap = Map(self.name + "_temp", seed=self.seed + 1, tilesize=self.tilesize, octaves=self.octaves * 3,
                           steps=6).save()

    def get_coord(self, x, y):
        """
        return the stats for the coord at (x, y)
        generates the tile if needed

        :param x:
        :param y:
        :return:
        """
        temp = self.tempmap.get_pixel(x, y)
        height = self.heightmap.get_pixel(x, y)

        return {"temperature": temp,
                "height": height,
                "biome": BIOMES[height][temp]}

    def save_biome_map(self, tile_x, tile_y):
        h = self.heightmap.get_tile(tile_x, tile_y).data
        t = self.tempmap.get_tile(tile_x, tile_y).data

        # print([str(x) for x in self.heightmap.get_tile(tile_x, tile_y) if x >=4])

        biome_stats = dict.fromkeys(COLORS.keys(), 0)

        biomes = []
        for x in range(len(h)):
            color = COLORS.get(BIOMES[h[x]][t[x]], "255   0   0")
            biome_stats[BIOMES[h[x]][t[x]]] += 1
            if color is "255   0   0":
                print("undefined for height %s and temp %s" % (h[x], t[x]))
            biomes.append(color)

        pixels = self.tilesize ** 2
        for stat in biome_stats:
            biome_stats[stat] = str((biome_stats[stat] * 100) / pixels)
        print("biomes in percent:")

        keys = sorted(biome_stats.keys())
        for k in keys:
            print(" %s: %s" % (k, biome_stats[k]))
        save_biome_as_ppm(self.name, biomes, tile_x, tile_y, self.tilesize)

    def pixel_to_tile_coords(self, pixel_x, pixel_y):
        """
        get the tilecoord a specific pixel is on

        :param pixel_x:
        :param pixel_y:
        :return: (tile_x, tile_y)
        """
        tile_x = int(pixel_x / self.tilesize)
        tile_y = int(pixel_y / self.tilesize)

        return tile_x, tile_y


def save_biome_as_ppm(name, vals, tile_x, tile_y, tilesize):
    with open("%s_%s_%s.pgm" % (name, tile_x, tile_y), 'wt') as f:
        f.write('P3\n')
        f.write('%s %s\n' % (tilesize, tilesize))  # width, height
        f.write('255\n')  # max greyval
        f.write('\n'.join(val for val in vals) + '\n')
