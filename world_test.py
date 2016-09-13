"""
get stats for a specific pixel in the world


will create tiles for a temperature and height map wich will not really be used right now.
they are just to see what basically happens.
"""


import argparse
from world.world import World

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("seed", type=int)
    parser.add_argument("x", type=int)
    parser.add_argument("y", type=int)
    parser.add_argument("--savetiles", action="store_true", default=False)
    args = parser.parse_args()


    w = World(args.name, args.seed, tilesize=128, octaves=5, savetiles=args.savetiles)

    print(w.get_coord(args.x, args.y))
    #w.save_biome_map(args.x, args.y)
