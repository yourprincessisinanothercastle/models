
import argparse
from models import db
from models.world import World
import time

from voronoi.voronoi import plot_voronoi, plot_delaunay
from models.constants import TILESIZE

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--dropdb", action="store_true", default=False)
    args = parser.parse_args()

    tilesize = TILESIZE

    if args.dropdb:
        db.drop_database('worldmap')
        exit(0)
    print('...')
    c = 0
    t_before = time.time()
    seed = 0
    coords = []
    biomes = []
    stats = {}
    w = World.objects.filter(name=str(seed)).first()
    if not w:
        #print(seed)
        w = World(str(seed), seed, tilesize=tilesize, octaves=5)
        w.save()
    for x in range(tilesize):
        for y in range(tilesize):
            d = w.get_coord(x, y)
            biome = d.get('height')
            coord = d.get('coord_on_map')
            coords.append(coord)
            biomes.append(biome)

    print('plotting voronoi')
    plot_voronoi(coords, biomes, 'vor_%s.png' % seed)
    plot_delaunay(coords, 'del_%s.png' % seed)
