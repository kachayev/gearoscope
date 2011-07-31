#!/usr/bin/env python
#
# Copyright 20011 Alexey S. Kachayev
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import distutils.core
import sys, os
# Importing setuptools adds some features like "setup.py develop", but
# it's optional so swallow the error if it's not there.
try:
    import setuptools
except ImportError:
    pass

kwargs = {}
version = '0.0.10'

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
        'License :: OSI Approved :: Apache License',
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

