import datetime
from django.db import models
from datetime import datetime
import random
# Create your models here.


class Server():

    def generateRecord(self):
        name = 'node%s' % random.randint(1,4)
        ping = random.randint(10, 1000)

        return {'server': name, 'host':'localhost', 'time': datetime.now().strftime('%H:%M') , 'ping': ping}

    def getData(self):

        return [self.generateRecord() for x in range(20)]


class Supervisor():

    def getNames(self):
        return ['apache', 'nginx', 'sonar', 'mysql', 'redis']

    def getStatuses(self):
        return ['running', 'stoped', 'restarting', 'crashed']

    def generateRecord(self):
        name = random.choice(self.getNames())
        pid = random.randint(10000, 30000)

        return {'name': name, 'host':'localhost', 'port': random.randint(100,1000), 'time': datetime.now().strftime('%H:%M'), 'status': random.choice(self.getStatuses())}

    def getData(self):

        return [self.generateRecord() for i in xrange(10)]


class Process():

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

        return [self.generateRecord() for i in xrange(20)]

        pass


    pass
