#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: R. Patrick Xian
"""

from __future__ import print_function
import numpy as np
from h5py import File


def copy(indir, infilename, outdir, outfilename=None, maxshape=(None,), chunks=(50000,),
           print_status=False, ret=None, **kwds):
    """ Carbon copy HDF5 files, including all groups and attributes.

    :Parameters:
        indir, infilename : raw string, raw string
            Input file directory and filename.
        outdir, outfilename : raw string, raw string | ..., None
            Output file directory and filename.
        maxshape : tuple/list | (None, )
            Maximum shape of the array stored as a dataset.
        chunks: tuple/list | (50000, )
            Chunk size of the files.
        print_status : bool | True
            Option to print the status of the file conversion (0 = Fail, 1 = Success).
        ret : str | None
            Return option (Set to ``'file'`` to return the file handle).
        **kwds : keyword arguments
            Additional arguments for ``h5py.File().create_dataset()``.
    """

    if outfilename is None:
        outfilename = infilename

    try:
        copied = 0
        f_in = File(indir + infilename, 'r')
        f_out = File(outdir + outfilename, 'w')

        # Copy global attributes
        for attrname, attrval in f_in.attrs.items():
            f_out.attrs[attrname] = attrval

        # Copy groups to the output file
        groups = list(f_in)
        for g in groups:

            f_out.create_dataset(g, data=f_in[g][:], maxshape=maxshape, chunks=chunks, **kwds)
            group_attrs = list(f_in[g].attrs)

            if len(group_attrs) > 0:
                # Copy attributes associated with the group
                for ga in group_attrs:
                    f_out[g].attrs.create(ga, f_in[g].attrs[ga])

        copied = 1

    except:
        pass

    finally:

        if print_status == True:
            print('Status = {}'.format(copied))

        try:
            # Close files after copying
            f_in.close()
            f_out.close()
        except:
            pass

    if ret is None:
        return
    elif ret == 'file':
        return f_out
