"""
Imlementation of sonar agent for pinging remove servers
and logging information about running status

Each of this agent will act in scope of general "ping" pooll,
in order to provide some trafeoff between fast responsein
multi-threading model, and using system resources for hanling
many separate threads.
"""

import re
from subprocess import Popep, PIPE
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

    STAT_LINE = re.compile(r'(?P<received>\d) received, (?P<lost>[\d]+)% packet loss, time (?P<time>[\d]+)ms')
    RTT_LINE  = re.compile(r'rtt min/avg/max/mdev = (?P<rtt>\S+) ms')

    def __init__(self, server):
        self.server = server

    def work(self):
        self.log = Log.buffer('ping')

        # Put into log buffer
        self.log.info(PingLogRecord(self.ping(4), server={'host': self.server.host}))

    def ping(count=4):
        stat = {}

        ping = '\n'.join(Popen(['ping', self.server.host, '-c', str(count)], stdout=PIPE).communicate())
        stat.update(STAT_LINE.findall(ping))
        stat.update(RTT_LINE.findall(ping))

        return stat

