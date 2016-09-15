"""
experiments
"""


import numpy as np
from scipy.spatial import Delaunay, Voronoi, voronoi_plot_2d, delaunay_plot_2d
import matplotlib.pyplot as plt


def spawn_shell():
    try:
        import bpython
        bpython.embed(locals_=dict(globals(), **locals()))
    except ImportError:
        pass

def plot_voronoi(coords_in, colors=None, filename=None):
    print('plotting...')
    coords = np.array(coords_in)
    vor = Voronoi(coords)
    # plot
    voronoi_plot_2d(vor)

    # colorize
    #spawn_shell()

    if colors:
        for x in range(len(vor.point_region)):
            region_nr = vor.point_region[x]
            color_str = colors[x]
            region = vor.regions[region_nr]
            if not -1 in region:
                polygon = [vor.vertices[i] for i in region]

                c = '%0.2X' % (color_str * int(255/6))
                print(c)
                plt.fill(*zip(*polygon), color='#' + c *3)


    #for region in vor.regions:
    #    print(region)
    #    if not -1 in region:
    #        polygon = [vor.vertices[i] for i in region]
    #        plt.fill(*zip(*polygon))
    plt.savefig(filename)

def plot_delaunay(coords, filename):
    print('plotting...')
    coords = np.array(coords)
    delaunay = Delaunay(coords)
    # plot
    delaunay_plot_2d(delaunay)

    plt.savefig(filename)


