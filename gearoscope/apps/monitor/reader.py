class Reader(object):
    '''Read log file, created by sonar daemon'''
    def __init__(self, path):
        self.path = path

    def tail(self, size, verbosity='info'):
        '''
        Return to client list of special Entry objects (one per each line in log)

        Method will reverse lines order as unix util `tail` done
        It also can filter entiries by verbosity level (will return higher)
        '''
        with open(self.path) as log:
            lines = [MonitorEntry.extract(line) for line in log.readlines()[::-1]]

            limit = MonitorEntry.LEVELS.index(verbosity.lower())
            lines = [entry for entry in lines if entry.code >= limit]

        return lines[:size]

class MonitorEntry(object):
    '''One line from log representation'''

    __slots__=('time', 'sender', 'level', 'code', 'message')

    LEVELS = ['debug', 'info', 'error', 'critical']

    def __init__(self, time, sender, level, message):
        self.time = time
        self.sender = sender.lower()
        self.level = level.lower()
        self.code = MonitorEntry.LEVELS.index(self.level)
        self.message = message.lower()

    @staticmethod
    def extract(line):
        '''Will cat from left side of line Time, Sender and Level marks'''
        parts = line.strip().split()
        return MonitorEntry(' '.join(parts[:2]), parts[2], parts[3], ' '.join(parts[4:]))

