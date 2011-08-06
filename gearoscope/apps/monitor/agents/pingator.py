"""
Imlementation of sonar agent for pinging remove servers
and logging information about running status

Each of this agent will act in scope of general "ping" pooll,
in order to provide some trafeoff between fast responsein
multi-threading model, and using system resources for hanling
many separate threads.
"""

import subprocess
from sonar.logger import DictLogRecord, Log

class PingLogRecord(DictLogRecord):
    '''Simple formatter for information about remote server'''
    scheme = {
        'from': '%(from)s',
        'status': '%(status)s'
    }

    def __init__(self, status, server=None):
        self.message['status'] = status
        self.message['from']   = server

    def __str__(self):
        if type(self.message['from']) == dict:
            self.message['from'] = self.format(**self.message['from'])

        return DictLogRecord.__str__(self)

class PingAgent(object):
    # Instance of in-memory buffer to persist responses log
    # This object will be created according to general application configuration
    # with "lazy" idea (when work method will be called only)
    log = None

    def __init__(self, server):
        self.server = server

    def work(self):
        self.log = Log.buffer('ping')

        # Put into log buffer
        self.log.info(PingLogRecord(self.ping(4), server={'host': self.server.host}))

    def ping(count=4):
        cmd = ['ping', self.server.host, '-c', str(count)]
        return subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[-1]

