import logging, random

from django.db import models
from datetime import datetime

class Server(object):

    def get_servers(self):
        return [{'name':['localhost', 'remote', 'linode', 'rabbit', 'db', 'load_balancer'][i], 'id': i} for i in xrange(1, 3)]

    def generate_record(self):
        serv = random.choice(self.get_servers())
        log_info = {'host': serv['name'],
                            'time': datetime.now().strftime('%H:%M:%S') ,
                            'ping': random.randint(10, 1000)}
        serv = dict(serv, **log_info)

        return serv

    def get_data(self):
        log = [self.generate_record() for x in range(10)]
        servers = self.get_servers()
        for server in servers:
            server['records'] = []
            for rec in log:
                if rec['id'] != server['id']:
                    continue
                server['records'].append(rec)
            server['records'].sort(key=lambda x: x['time'])

        return servers


class Supervisor(object):

    def getNames(self):
        return ['apache', 'nginx', 'sonar', 'mysql', 'redis']

    def getStatuses(self):
        return ['running', 'stoped', 'restarting', 'crashed']

    def generateRecord(self):
        name = random.choice(self.getNames())
        pid = random.randint(10000, 30000)

        return {'name': name, 'host':'localhost', 'port': random.randint(100, 1000), 'time': datetime.now().strftime('%H:%M:%S'), 'status': random.choice(self.getStatuses())}

    def getData(self):

        return [self.generateRecord() for i in xrange(10)]


class Process(object):

    def generateRecord(self):

        return {
            'username': random.choice(['root', 'www-data']),
            'mem': random.randint(0, 100),
            'pid': random.randint(10000, 30000),
            'cmdline' : 'pythonenv_stub/workers/reverse.py',
            'is_running': True,
            'cpu': random.randint(0, 100),
            'host': '127.0.0.1',
            'name': random.choice(Supervisor().getNames()),
        }

        pass

    def getData(self):

        return [self.generateRecord() for i in xrange(10)]

        pass


    pass


class Workers(object):

    def get_workers(self):
        return [{'name':random.choice(['worker', 'tasker', 'trans']), 'id': i} for i in xrange(1, 4)]

    def get_data(self, id):

        return {'cpu_value': random.randint(0, 100),
                'memory_value': random.randint(0, 100),
                'task_value': random.randint(10, 40)
            }

        pass

