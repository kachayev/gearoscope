import tests.settings as settings

from time import sleep
from gearman import GearmanWorker

class SleepingGearmanWorker(GearmanWorker):
    def after_poll(self, activity):
        sleep(settings.STUB_WORKERS_FREQUENCY)
        return True

# This object will be used by all worker scripts
worker = SleepingGearmanWorker(settings.STUB_GEARMAN_NODES)

