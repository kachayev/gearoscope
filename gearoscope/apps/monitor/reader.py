class Reader(object):
    def __init__(self, path):
        self.path = path

    def tail(self, size, verbosity='info'):
        with open(self.path) as log:
            lines = [MonitorEntry.extract(line) for line in log.readlines()[::-1]]

            limit = MonitorEntry.LEVELS.index(verbosity.lower())
            lines = [entry for entry in lines if entry.code >= limit]

        return lines[:max(size,len(lines))]

class MonitorEntry(object):
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
        parts = line.strip().split()
        return MonitorEntry(' '.join(parts[:2]), parts[2], parts[3], ' '.join(parts[4:]))

