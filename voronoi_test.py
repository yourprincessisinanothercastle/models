import argparse
import time

from models import db
from models.constants import TILESIZE


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--dropdb", action="store_true", default=False)
    parser.add_argument('x', type=int)
    parser.add_argument('y', type=int)
    args = parser.parse_args()

    if args.dropdb:
        db.drop_database('worldmap')
        exit(0)

    w = VoronoiWorld('test')
    print(w.get_point_data(args.x, args.y))
