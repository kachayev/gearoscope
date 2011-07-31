import operator

from sonar.logger import DictLogRecord, Log
from sonar.options import options
from gearman import GearmanAdminClient, errors as GearmanErrors

class StatusLogRecord(DictLogRecord):
    '''
    Formatter for information about general gearman node status,
    aggregate workers and queues field for this
    '''
    scheme = {
        'queues': '%(queues)s',
        'workers': '%(workers)s',
    }

    def __str__(self):
        queues  = len(self.message)
        workers = reduce(operator.add, [int(q['workers']) for q in self.message], 0)

        self.message = {'queues': queues, 'workers': workers}
        return DictLogRecord.__str__(self)

class QueueLogRecord(DictLogRecord):
    '''Simple formatter for information about one running queue'''
    scheme = {
        'task': '%(task)s',
        'workers': '%(workers)s',
        'running': '%(running)s',
        'queued': '%(queued)s',
    }

    def __str__(self):
        return DictLogRecord.__str__(self)


class GearmanNodeAgent(object):
    """
    GearmanNodeAgent will connect to remote running gearmand daemon via socket interface to gearman-admin,
    retrieve information about queues and workers, calculate general node state
    """
    # Instance of gearman admin client
    # In case of connection error, special message will be wrote to log file
    client = None

    # Instance of in-memory buffer to persist responses log
    # This object will be created according to general application configuration
    # with "lazy" idea (when work method will be called only)
    log = None

    def __init__(self, server, port):
        self.server = server
        self.port = port

    def work(self):
        """
        Should collect information about all queues and workers per each gearman node
        In future this information will be used  for collecting and grouping informations
        by running queues (with average load) and running worker processes
        """
        self.log = Log.buffer('gearman', options.config.get('agent:gearman', 'log_buffer_file'))

        try:
            # Lazy connection if necessary...
            self.client = self.client or GearmanAdminClient(['%s:%s' % (self.server.host, self.port)])

            # Retrieve status information via socket connection
            status = self.client.get_status()

            # Put into log buffer
            self.log.info(StatusLogRecord(status))
            for queue in status:
                self.log.info(QueueLogRecord(queue))

        except GearmanErrors.ServerUnavailable, e:
            # Such error can be raised in two cases:
            # 1. gearmand is not running (stopped by user or crashed with error)
            # 2. socket client doesn't work normaly, for example cause of network problems
            # In any case, we can't retrieve more information here,
            # so you have to resolve this issue manually
            self.log.error(e)

