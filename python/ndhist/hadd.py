from ndhist.hist import Hist, is_h5_hist
from h5py import File

def _add_tree(base, new):
    for name, sub in new.items():
        # if sub is a hist, add it to base
        if is_h5_hist(sub):
            if name not in base:
                base[name] = Hist(sub)
            else:
                base[name] += Hist(sub)
        # otherwise sub is a group
        else:
            if name not in base:
                base[name] = {}
            _add_tree(base[name], sub)

def _build_h5_tree(base_group, base_dic):
    for name, sub in base_dic.items():
        assert name not in base_group
        # if the sub is a dic, create a group
        if isinstance(sub, dict):
            subgroup = base_group.create_group(name)
            _build_h5_tree(subgroup, sub)
        # otherwise, assume it's a hist
        else:
            sub.write(base_group, name)

def hadd(out_file_name, file_itr, verbose=False):
    # build up the tree
    htree = {}
    for fname in file_itr:
        if verbose:
            print('adding {}'.format(fname))
        with File(fname, 'r') as infile:
            _add_tree(htree, infile)

    # now write out
    with File(out_file_name, 'w') as outfile:
        _build_h5_tree(outfile, htree)
