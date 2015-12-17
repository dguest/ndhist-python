import numpy as np
import math

# __________________________________________________________________________
# Hist class from ndhist
def is_h5_hist(base):
    return hasattr(base, 'attrs') and 'axes' in base.attrs

class Hist:
    """very simple wrapper for histogram info"""
    def __init__(self, base):
        self.hist = np.asarray(base)
        try:
            self.axes = get_axes(base)
        except KeyError as err:
            raise OSError("{} doesn't seem to be a histogram".format(
                str(base)))
    def __str__(self):
        return '{}-dim hist'.format(len(self.axes))
    def __repr__(self):
        axes = ' vs '.join([x.name for x in self.axes])
        return 'Histogram[{}]'.format(axes)

def get_axes(ds):
    """returns a list of axes from a Dataset produced via ndhist"""
    axes_ar = ds.attrs['axes']
    ax_props = axes_ar.dtype.names
    axes = []
    for ax in axes_ar:
        the_ax = Axis(ax_props, ax)
        axes.append(the_ax)
    return axes

class Axis:
    def __init__(self, prop_list, array):
        self.name = array[prop_list.index('name')]
        self.lims = [array[prop_list.index(x)] for x in ['min', 'max']]
        self.units = array[prop_list.index('units')]
    def __str__(self):
        prints = [self.name] + list(self.lims) + [self.units]
        return 'name: {}, range: {}-{}, units {}'.format(
            *(str(x) for x in prints))
