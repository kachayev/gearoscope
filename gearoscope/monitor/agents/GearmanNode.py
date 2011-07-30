import operator

from gearman import GearmanAdminClient, errors as GearmanErrors

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
            self.client = self.client or GearmanAdminClient(['%s:%s' % (self.server.host, self.port)])
        except GearmanErrors.ServerUnavailable, e:
            self.log.error(e)

