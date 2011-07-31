"""
sonard -- daemon process which use Sonar library for launching several monitoring agents in separated threads

Usage: python manage.py startsonar [options]

Options [sonard]:
-n --no-daemon  Do not use process daemonizing
-c --config     Path to configuration file
-p --pid-file   Path to daemon pid file
-v --verbose    Logging (verbosity) level
"""

import sys

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from sonar import loop
from sonar.logger import Log
from sonar.options import options

from monitor.sonard import sonar_factory

# Define setting options for sonar fabric in order to resolve problems
# with unrecognized options in arguments list
options.define('--settings', '-s')

# Set manually configuration param for runnig sonar daemon
sys.argv.append('--config=%s' % settings.SONAR_CONFIGURATION_FILE)

class Command(BaseCommand):
    '''
    Start sonar-based monitoring daemon

    Overrided buffer file for Log object in order to give to user
    possibility not to duplication logging configuration in
    several config files
    '''
    help = __doc__

    def handle(self, *args, **options):
        Log.BUFFER_FILE = settings.SONAR_LOG_FILE
        loop.main(factory=sonar_factory())

