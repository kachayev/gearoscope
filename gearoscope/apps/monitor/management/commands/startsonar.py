#!/usr/bin/env python

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from monitor.sonard import sonar_factory

class Command(BaseCommand):
    def handle(self, *args, **options):
        Log.BUFFER_FILE = settings.SONAR_CONFIGURATION_FILE
        loop.main(factory=sonar_factory())
        self.stdout.write('Successfully closed poll \n')

