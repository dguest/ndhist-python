import numpy as np
import math
import copy

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
            # save the dtype for later use
            self._ax_dtype = _get_axes_type(base)
        except KeyError as err:
            raise OSError("{} doesn't seem to be a histogram".format(
                str(base)))
    def __str__(self):
        return '{}-dim hist'.format(len(self.axes))
    def __repr__(self):
        axes = ' vs '.join([x.name for x in self.axes])
        return 'Histogram[{}]'.format(axes)

    # various convenience add operators
    def __add__(self, other):
        out = copy.deepcopy(self)
        out += other
        return out
    def __radd__(self, other):
        if other == 0: # check for sum()
            return self
        return self + other
    def __iadd__(self, other):
        self.hist += other.hist
        return self

    # for saving
    def _axes_as_numpy(self):
        tuples = [ax.as_tuple(self._ax_dtype.names) for ax in self.axes]
        return np.array(tuples, dtype=self._ax_dtype)
    def write(self, group, name):
        ds = group.create_dataset(name, data=self.hist)
        ds.attrs['axes'] = self._axes_as_numpy()
        pass


def get_axes(ds):
    """returns a list of axes from a Dataset produced via ndhist"""
    axes_ar = ds.attrs['axes']
    ax_props = axes_ar.dtype.names
    axes = []
    for ax in axes_ar:
        the_ax = Axis(ax_props, ax)
        axes.append(the_ax)
    return axes

def _get_axes_type(ds):
    return ds.attrs['axes'].dtype

class Axis:
    def __init__(self, prop_list, array):
        self.name = array[prop_list.index('name')]
        self.lims = [array[prop_list.index(x)] for x in ['min', 'max']]
        self.units = array[prop_list.index('units')]
        self._nbins = array[prop_list.index('n_bins')]
    def __str__(self):
        prints = [self.name] + list(self.lims) + [self.units]
        return 'name: {}, range: {}-{}, units {}'.format(
            *(str(x) for x in prints))
    def as_tuple(self, names):
        """Return a tuple organized by names. Mostly for serialization."""
        store = {'name': self.name, 'n_bins': self._nbins,
                 'min': self.lims[0], 'max': self.lims[1],
                 'units': self.units}
        return tuple([store[name] for name in names])


