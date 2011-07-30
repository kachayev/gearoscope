import tests.settings as settings

from sleeping import worker

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

# Setting client ID can be useful for analyzing information
# from gearman admin client, which show list of
# currently connected workers by its CLIENT ID
worker.set_client_id(settings.STUB_WORKERS_ID_FORMAT % {'task': 'reverse'})
worker.register_task('reverse', task_listener)

# Run worker in infinitive loop
worker.work()

