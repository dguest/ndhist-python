import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from ndhist.hist import Hist
from matplotlib.patches import Patch
import os

def draw_rgb(red, green, blue, axes, out_path, leg):
    rgb = np.dstack([red, green, blue])
    # crop off overflow
    rgb = rgb[1:-1, 1:-1,:]
    rgb = np.log1p(rgb)
    for iii in range(rgb.shape[2]):
        maxval = nth_largest(rgb[:,:,iii], 2)
        rgb[:,:,iii] = np.minimum(rgb[:,:,iii] / maxval, 1)
    fig = Figure(figsize=(5.0,5.0*3/4))
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(1,1,1)
    xlims, ylims = axes[0].lims, axes[1].lims
    imextent = list(xlims) + list(ylims)
    # transpose arrays so they draw properly (weird property of imshow)
    ax.imshow(rgb.swapaxes(0,1), interpolation='nearest',
              origin='lower', extent=imextent, aspect='auto')
    ax.set_xlim(*xlims)
    ax.set_ylim(*ylims)
    _label_axes(ax, axes)
    _add_rgb_legend(ax, leg)
    out_dir, out_file = os.path.split(out_path)
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    print('printing {}'.format(out_path))
    canvas.print_figure(out_path, bbox_inches='tight')

def _label_axes(ax, axes, size=12):
    xunit = axes[0].units
    yunit = axes[1].units
    ax.set_xlabel(axis_name(axes[0], xunit), x=0.98, ha='right', size=size)
    ax.set_ylabel(axis_name(axes[1], yunit), y=0.98, ha='right', size=size)

def _add_rgb_legend(ax, leg):
    rgb_patch = [Patch(color=x) for x in 'rgb']
    bcl_names = [leg[x] for x in ['red', 'green', 'blue']]
    title = None
    ax.legend(rgb_patch, bcl_names, loc='upper right', fancybox=False,
              borderaxespad=0.2, title=title, framealpha=0.5,
              labelspacing=0.2, handlelength=1.0)

def nth_largest(array, n):
    # check for float, if that's what it is, treat it as a fraction of
    # array length
    if n % 1 != 0:
        n = math.ceil(len(array) * n)
    return np.sort(array.flatten())[-n]

def axis_name(ax, units):
    nm, un = ax.name, units
    return '{} [{}]'.format(nm, un) if un else nm
