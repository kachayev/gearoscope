#!/usr/bin/env python
#
# Gearoscope is a gearman server monitoring and gearman worker management system
# Copyright (C) 2011 Alexey S. Kachayev, Iurii Ogiienko
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import distutils.core
import sys, os

# Importing setuptools adds some features like "setup.py develop", but
# it's optional so swallow the error if it's not there.
try:
    import setuptools
except ImportError:
    pass

kwargs = {}
version = '0.0.12'

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
    requirements = [line.strip() for line in f.readlines() if line.strip() != '' and line.strip()[:2] != '-e']

distutils.core.setup(
    name='gearoscope',
    packages = setuptools.find_packages(),
    version = version,
    install_requires=requirements,
    description = 'Gearman server monitoring and gearman worker management system',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Development',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPL v3',
        'Operating System :: POSIX',
        'Programming Language :: Python',
    ],
    author = 'Alexey S. Kachayev',
    author_email = 'kachayev@gmail.com',
    url='http://pypi.python.org/pypi/gearoscope',
    download_url = 'https://github.com/kachayev/gearoscope/',
    license='http://www.apache.org/licenses/LICENSE-2.0',
    **kwargs
)

