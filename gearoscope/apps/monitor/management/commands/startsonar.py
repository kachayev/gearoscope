import sys

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from sonar import loop
from sonar.logger import Log
from sonar.options import options

from monitor.sonard import sonar_factory

options.define('--settings', '-s')
sys.argv.append('--config=%s' % settings.SONAR_CONFIGURATION_FILE)

class Command(BaseCommand):
    help = 'Start sonar-based monitoring daemon'

    def handle(self, *args, **options):

        Log.BUFFER_FILE = settings.SONAR_LOG_FILE
        loop.main(factory=sonar_factory())

