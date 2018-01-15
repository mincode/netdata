# encoding: utf-8
"""Path utility functions."""

# Copyright (c) 2016-present, Manfred Minimair
# All rights reserved.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This file is derived from jupyter_core.paths, which is
# copyright (c) Jupyter Development Team
# and distributed under the terms of the Modified BSD License,
# and derived from IPython.utils.path, which is
# copyright (c) IPython Development Team
# and distributed under the terms of the Modified BSD License.


import os


def get_home_dir():
    """Get the real path of the home directory"""
    home_dir = os.path.expanduser('~')
    # Next line will make things work even when /home/ is a symlink to
    # /usr/home as it is on FreeBSD, for example
    home_dir = os.path.realpath(home_dir)
    return home_dir
