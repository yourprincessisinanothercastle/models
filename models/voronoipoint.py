from mongoengine import StringField, Document, IntField, ReferenceField, ListField, FloatField

import numpy as np
from scipy.spatial import Delaunay, Voronoi
import json
import random
import time

class VoronoiPoint(Document):
    world = ReferenceField('World', unique_with=['tile_coordinate_x', 'tile_coordinate_y'], required=True)
    tile_coordinate_x = IntField(required=True)
    tile_coordinate_y = IntField(required=True)

    _shape = ListField(FloatField())
    _neighbors = ListField(ListField(IntField()))
    _part_of_biome = ListField(ReferenceField('VoronoiPoint'))

    def __init__(self, world, tile_coordinate_x, tile_coordinate_y, *args, **kwargs):
        Document.__init__(self, *args, **kwargs)
        self.tile_coordinate_x = tile_coordinate_x
        self.tile_coordinate_y = tile_coordinate_y
        self.world = world


    @property
    def voronoi_coord(self):
        return self._get_coord_on_voronoi(self.tile_coordinate_x, self.tile_coordinate_y)

    @property
    def neighbors(self):
        t_before = time.time()
        n = self._get_neighbors(self.tile_coordinate_x, self.tile_coordinate_y)
        t_after = time.time()
        print('took %s' % (t_after - t_before))
        return n

    @property
    def shape(self):
        return self._get_shape(self.tile_coordinate_x, self.tile_coordinate_y)

    @property
    def shape_size(self):
        return self._get_shapesize(self.tile_coordinate_x, self.tile_coordinate_y)

    def _get_rows_around(self, x_on_tilemap, y_on_tilemap):
        x = x_on_tilemap
        y = y_on_tilemap

        row_count = 3
        x_range = range(x - row_count, x + row_count)
        y_range = range(y - row_count, y + row_count)

        coords = []
        for x in x_range:
            for y in y_range:
                coords.append((x, y))
        return coords

    def _find_in_array(self, item, array):
        """
        return index of element in array

        :param item:
        :param array:
        :return:
        """
        index = 0
        for i in list(array):
            if list(i) == list(item):
                return index
            index += 1
        return False

    def _get_coord_on_voronoi(self, x_on_tilemap, y_on_tilemap):
        """
        get pixelcoordinates for voronoi map out of pixel coords of tilemap

        :param x_on_tilemap:
        :param y_on_tilemap:
        :return:
        """
        factor = 20
        r = random.Random(self.world.seed + 10 * x_on_tilemap + y_on_tilemap)
        x = x_on_tilemap * factor + r.randint(0, factor)
        if y_on_tilemap % 1 == 0:
            y = y_on_tilemap * factor + r.randint(0, factor)
        else:
            y = y_on_tilemap * factor + factor / 2 + r.randint(0, factor)
        return x, y

    def _get_shape(self, x_on_tilemap, y_on_tilemap):
        if self._shape:
            return self._shape
        else:
            coords_on_tilemap = self._get_rows_around(x_on_tilemap, y_on_tilemap)
            coords = []
            for c in coords_on_tilemap:
                coords.append(self._get_coord_on_voronoi(*c))

            coords = np.array(coords, dtype=(float, 2))

            # create the voronoi diagram
            vor = Voronoi(coords)

            # find the index of our coords in the points array
            index = self._find_in_array(self._get_coord_on_voronoi(x_on_tilemap, y_on_tilemap), array=vor.points)

            # f = np.where(vor.points == (self.get_coord_on_voronoi(x_on_tilemap, y_on_tilemap)))
            # print(f)

            # get the corresponding region for our point
            region_nr = vor.point_region[index]

            # the points which define the region are listes in regions, but the coords are in verticies
            polygon = [tuple(vor.vertices[i]) for i in vor.regions[region_nr]]
            self._shape = polygon
        return self._shape

    def _get_neighbors(self, x_on_tilemap, y_on_tilemap):
        """
        get neighbors of search_coord

        :param coords: list of tuples
        :param coords: tuple (should be in coords)
        :return:
        """

        """
        TODO: this probably needs testing. not sure if the indexes are consistent.
        """
        if self._neighbors:
            return self._neighbors

        else:
            coords_on_tilemap = self._get_rows_around(x_on_tilemap, y_on_tilemap)
            coords = []
            for c in coords_on_tilemap:
                coords.append(self._get_coord_on_voronoi(*c))

            d = Delaunay(np.array(coords))

            index = self._find_in_array(self._get_coord_on_voronoi(x_on_tilemap, y_on_tilemap), array=d.points)

            neighbor_indicies = set()
            for x in d.vertices:
                if index in x:
                    for element in x:
                        if element != index:
                            neighbor_indicies.add(element)

            self._neighbors = [coords_on_tilemap[n] for n in neighbor_indicies]
            self.save()
        return self._neighbors

    def get_point_data(self, x, y):
        return json.dumps({
            "shape": list(self._get_shape(x, y)),
            "shape_size": self._get_shapesize(x, y),
            "neighbors": self._get_neighbors(x, y),
            "biome": self.world.get_biome(x, y),
            "height": self.world.get_height(x, y),
            "temperature": self.world.get_temperature(x, y),
            "position_on_map": list(self._get_coord_on_voronoi(x, y))
        })

    def _get_shapesize(self, x_on_tilemap, y_on_tilemap):
        def area(p):
            return 0.5 * abs(sum(x0 * y1 - x1 * y0
                                 for ((x0, y0), (x1, y1)) in segments(p)))

        def segments(p):
            return zip(p, p[1:] + [p[0]])

        x = x_on_tilemap
        y = y_on_tilemap
        shape = self._get_shape(x, y)
        return area(shape)

    def _plot_voronoi(self, tile_x, tile_y, filename=None):
        """
        debug output only

        :param coords_in:
        :param colors:
        :param filename:
        :return:
        """
        from scipy.spatial import voronoi_plot_2d
        import matplotlib.pyplot as plt

        coords = []
        colors = []

        # convert coords to voronoi coords, get height
        s = self.world.tilesize
        for x in range(s):
            for y in range(s):
                coords.append(
                    self._get_coord_on_voronoi(
                        (tile_x * s) + x, (tile_y * s) + y))
                colors.append(
                    self.world.heightmap.get_pixel((tile_x * s) + x, (tile_y * s) + y))

        # create and plot the voronoi
        vor = Voronoi(coords)
        # plot
        voronoi_plot_2d(vor)

        # colorize
        # spawn_shell()

        if colors:
            for x in range(len(vor.point_region)):
                region_nr = vor.point_region[x]
                color_str = colors[x]
                region = vor.regions[region_nr]
                if not -1 in region:
                    polygon = [vor.vertices[i] for i in region]

                    c = '%0.2X' % (color_str * int(255 / 6))
                    plt.fill(*zip(*polygon), color='#' + c * 3)

        # for region in vor.regions:
        #    print(region)
        #    if not -1 in region:
        #        polygon = [vor.vertices[i] for i in region]
        #        plt.fill(*zip(*polygon))
        plt.savefig('%s_voronoi_%s_%s.png' % (self.world.name, tile_x, tile_y))

    def _plot_delaunay(self, tile_x, tile_y):
        """
        debug output only

        :param coords:
        :param filename:
        :return:
        """
        from scipy.spatial import delaunay_plot_2d
        import matplotlib.pyplot as plt

        coords = []

        # convert coords to voronoi coords, get height
        s = self.world.tilesize
        for x in range(s):
            for y in range(s):
                coords.append(
                    self._get_coord_on_voronoi(
                        (tile_x * s) + x, (tile_y * s) + y))


        print('plotting...')
        coords = np.array(coords)
        delaunay = Delaunay(coords)
        # plot
        delaunay_plot_2d(delaunay)

        plt.savefig('%s_delaunay_%s_%s.png' % (self.world.name, tile_x, tile_y))
