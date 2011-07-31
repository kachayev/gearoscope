class Reader(object):
    def __init__(self, path):
        self.path = path

    def tail(self, size, verbosity='INFO'):
        with open(self.path) as log:
            lines = [line.strip() for line in log.readlines[::-1] if line.find(verbosity) != -1]

        return lines

reader = Reader('/tmp/ps.log')

