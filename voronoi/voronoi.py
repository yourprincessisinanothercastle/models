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



