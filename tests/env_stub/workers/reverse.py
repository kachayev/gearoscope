import tests.settings as settings

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

