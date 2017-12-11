# encoding: utf-8
"""Path utility functions."""

# Copyright (c) 2016, Manfred Minimair
# Distributed under the terms of the Modified BSD License.

# Derived from jupyter_core.paths, which is
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Derived from IPython.utils.path, which is
# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.


import os


def get_home_dir():
    """Get the real path of the home directory"""
    home_dir = os.path.expanduser('~')
    # Next line will make things work even when /home/ is a symlink to
    # /usr/home as it is on FreeBSD, for example
    home_dir = os.path.realpath(home_dir)
    return home_dir
