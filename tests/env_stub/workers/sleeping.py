import tests.settings as settings

from time import sleep
from gearman import GearmanWorker

class SleepingGearmanWorker(GearmanWorker):
    '''
    Extend standard gearman worker facilities, adding sleeping tic after each jobs poll

    You can use `after_poll` method to add some additional facilities to runnig worker,
    for example logging, notification and something like this
    '''
    def after_poll(self, activity):
        '''
        Called by parent gearman worker after each poll
        (we assump that worker is running in loop and can handle serveral jobs worload)

        True is return in order "to say" to worker get next job
        '''
        sleep(settings.STUB_WORKERS_FREQUENCY)
        return True

# This object will be used by all worker scripts
worker = SleepingGearmanWorker(settings.STUB_GEARMAN_NODES)

def run(task_name, task_listener, worker=worker):
    '''
    Customize worker and register workload function
    and then run worker in infinitive loop

    Can be simply reusing in each worker script
    '''
    worker.set_client_id(settings.STUB_WORKERS_ID_FORMAT % {'task': task_name})
    worker.register_task(task_name, task_listener)
    worker.work()

