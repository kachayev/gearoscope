import os, sys

# Working directory (current file one)
WORKDIR = os.path.join(os.path.dirname(__file__), '..', '..', '..')

# This will give us oppurtunities to keep applications in separated directory
# and prevent chaus in main project directory
sys.path.append(os.path.join(WORKDIR, '..'))

import operator
import gearoscope.tests.settings as settings

from sleeping import run

def task_listener(gearman_worker, gearman_job):
    '''
    Per each poll from gearman node,
    worker will call this function and give context params: worker and job
    '''
    done = reduce(operator.mul, [int(x) for x in gearman_job.data.split('*')], 1)

    # Log result of multipling digits in order to control worker activity
    # Returned result should be a string
    # TODO: logging!
    print '%s = <%d>' % (gearman_job.data, done)
    return str(done)

run('multiple', task_listener)

