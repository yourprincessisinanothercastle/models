from .map import Map
import json
from collections import OrderedDict
import operator

import argparse

# http://www-cs-students.stanford.edu/~amitp/game-programming/polygon-map-generation/#biomes
BIOMES = [[0 for x in range(6)] for y in range(5)]  # will have coords: height, moisture

BIOMES[0][0] = "water"  # dry, low
BIOMES[0][1] = "water"
BIOMES[0][2] = "water"
BIOMES[0][3] = "ice"
BIOMES[0][4] = "ice"
BIOMES[0][5] = "ice"

BIOMES[1][0] = "subtropical_desert"  # dry, low
BIOMES[1][1] = "grassland"
BIOMES[1][2] = "tropical_seasonal_forest"
BIOMES[1][3] = "tropical_seasonal_forest"
BIOMES[1][4] = "tropical_rainforest"
BIOMES[1][5] = "tropical_rainforest"

BIOMES[2][0] = "temperate desert"
BIOMES[2][1] = "grassland"
BIOMES[2][2] = "grassland"
BIOMES[2][3] = "temperate_deciduous_forest"
BIOMES[2][4] = "temperate_deciduous_forest"
BIOMES[2][5] = "temperate_rain_forest"

BIOMES[3][0] = "temperate_desert"
BIOMES[3][1] = "temperate_desert"
BIOMES[3][2] = "shrubland"
BIOMES[3][3] = "shrubland"
BIOMES[3][4] = "taiga"
BIOMES[3][5] = "taiga"

BIOMES[4][0] = "scorched"
BIOMES[4][1] = "bare"
BIOMES[4][2] = "tundra"
BIOMES[4][3] = "snow"
BIOMES[4][4] = "snow"
BIOMES[4][5] = "snow"

COLORS = {
    "snow":                         "255 255 255",
    "tundra":                       "221 221 187",
    "bare":                         "187 187 187",
    "scorched":                     "153 153 153",
    "taiga":                        "204 212 187",
    "shrubland":                    "196 204 187",
    "temperate_desert":             "228 232 202",
    "temperate_rain_forest":        "164 196 168",
    "temperate_deciduous_forest":   "180 201 169",
    "grassland":                    "196 212 170",
    "subtropical_desert":           "233 221 199",
    "temperate desert":             "228 232 202",
    "tropical_rainforest":          "156 187 169",
    "tropical_seasonal_forest":     "169 204 164",
    "ice":                          "0   0   128",
    "water":                        "0   0   255"
}


class World():
    def __init__(self, name, seed, tilesize=256, octaves=3):
        self.heightmap = Map(name + "_height", seed=seed, tilesize=tilesize, octaves=octaves, granularity=5)
        self.tempmap = Map(name + "_temp", seed=seed + 1, tilesize=tilesize, octaves=octaves * 2,
                           granularity=6)  # octaves * 2 = bigger temperature blobs

        self.tilesize = tilesize
        self.name = name

    def get_coord(self, x, y):
        temp = self.tempmap.get_pixel(x, y)
        height = self.heightmap.get_pixel(x, y)

        return {"temperature": temp,
                "height": height,
                "biome": BIOMES[height][temp]}

    def save_biome_map(self, tile_x, tile_y):
        h = self.heightmap.get_tile(tile_x, tile_y)
        t = self.tempmap.get_tile(tile_x, tile_y)

        # print([str(x) for x in self.heightmap.get_tile(tile_x, tile_y) if x >=4])

        biome_stats = dict.fromkeys(COLORS.keys(), 0)

        biomes = []
        for x in range(len(h)):
            color = COLORS.get(BIOMES[h[x]][t[x]], "255   0   0")
            biome_stats[BIOMES[h[x]][t[x]]] += 1
            if color is "255   0   0":
                print("undefined for height %s and temp %s" % (h[x], t[x]))
            biomes.append(color)

        pixels = self.tilesize**2
        for stat in biome_stats:
            biome_stats[stat] = str((biome_stats[stat] * 100) / pixels)
        print("biomes in percent:")

        keys = sorted(biome_stats.keys())
        for k in keys:
            print(" %s: %s" % (k, biome_stats[k]))
        save_biome_as_ppm(self.name, biomes, tile_x, tile_y, self.tilesize)


def save_biome_as_ppm(name, vals, tile_x, tile_y, tilesize):
    with open("%s_%s_%s.pgm" % (name, tile_x, tile_y), 'wt') as f:
        f.write('P3\n')
        f.write('%s %s\n' % (tilesize, tilesize))  # width, height
        f.write('255\n')  # max greyval
        f.write('\n'.join(val for val in vals) + '\n')
