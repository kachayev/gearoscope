import operator
import tests.settings as settings

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

