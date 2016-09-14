"""
get stats for a specific pixel in the world


will create tiles for a temperature and height map wich will not really be used right now.
they are just to see what basically happens.
"""


import argparse
import models
from models.world import World
import time

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("seed", type=int)
    parser.add_argument("x", type=int)
    parser.add_argument("y", type=int)
    parser.add_argument("--savetiles", action="store_true", default=False)
    args = parser.parse_args()

    tilesize = 64

    w = World.objects.filter(name=args.name).first()
    if not w:
        w = World(args.name, args.seed, tilesize=tilesize, octaves=5)
        w.save()

    c = 0
    t_before = time.time()

    for x in range(10):
        for y in range(10):
            print(w.get_coord(x*tilesize, y*tilesize))
            c+=1

    print('created %s tiles (%s ^2) in %s seconds' % (c, tilesize, time.time()-t_before))
    #w.save_biome_map(args.x, args.y)
