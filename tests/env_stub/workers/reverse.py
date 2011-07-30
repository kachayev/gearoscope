import os, sys

# Working directory (current file one)
WORKDIR = os.path.join(os.path.dirname(__file__), '..', '..', '..')

# This will give us oppurtunities to keep applications in separated directory
# and prevent chaus in main project directory
sys.path.append(os.path.join(WORKDIR, '..'))

import gearoscope.tests.settings as settings

from sleeping import run

def task_listener(gearman_worker, gearman_job):
    '''
    Per each poll from gearman node,
    worker will call this function and give context params: worker and job
    '''
    done = gearman_job.data[::-1]

    # Log result of string reversing in order to control worker activity
    # TODO: logging!
    print 'Done <%s>' % done
    return done

run('reverse', task_listener)

