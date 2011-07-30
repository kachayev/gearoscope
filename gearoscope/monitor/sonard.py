#!/usr/bin/env python

"""
sonard -- daemon process which use Sonar library for launching several monitoring agents in separated threads

Usage: %s [options]

Options:
-n --no-daemon  Do not use process daemonizing
-c --config     Path to configuration file
-p --pid-file   Path to daemon pid file
-v --verbose    Logging (verbosity) level
"""

from sonar import loop
from sonar.sonard import sonar_factory

if __name__ == '__main__':
    loop.main(factory=sonar_factory())

