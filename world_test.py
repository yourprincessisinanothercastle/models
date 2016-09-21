"""
get stats for a specific pixel in the world


will create tiles for a temperature and height map wich will not really be used right now.
they are just to see what basically happens.
"""


import argparse
from models import db
from models.world import World
import time

from models.constants import TILESIZE

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dropdb", action="store_true", default=False)
    args = parser.parse_args()

    tilesize = TILESIZE

    if args.dropdb:
        db.drop_database('worldmap')
        exit(0)

    c = 0
    t_before = time.time()
    seed = 0
    coord = {}
    stats = {}
    while coord.get('biome', '') != ('ice' or 'water'):


        coord = w.get_coord(0, 0)
        seed += 1
        if not stats.get(coord['biome'], False):
            stats[coord['biome']] = 0
        stats[coord['biome']] += 1
        w._save_biome_map(0, 0)
        if seed % 100 == 0:
            print('100 worlds later... (%s)' % seed)
        if seed % 100 == 0:
            print(stats)

    print('seed: %s' % seed)
    print(coord)


    #for x in range(100):
    #    for y in range(100):
    #        print(w.get_coord(x, y))
    #        c+=1

    print('created %s tiles (%s ^2) in %s seconds' % (c, tilesize, time.time()-t_before))
    #w.save_biome_map(args.x, args.y)
