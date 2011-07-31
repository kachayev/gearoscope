import logging, random
import re

from django.db import models
from datetime import datetime

import random

class Process(object):
    """
        I am just stub
    """
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
    """
        I am another one stub
    """
    def get_workers(self):
        return [{'name':random.choice(['worker', 'tasker', 'trans']), 'id': i} for i in xrange(1, 4)]

    def get_data(self, id):

        return {'cpu_value': random.randint(0, 100),
                'memory_value': random.randint(0, 100),
                'task_value': random.randint(10, 40)
            }

        pass





class ServerLogReader(object):
    log = []

    def __init__(self, reader):
        ServerLogReader.log = reader.tail(10000)

    def get_records_for(self, server):
#        TODO: implement server reader
        for entry in ServerLogReader.log:
            logging.error(entry)
            pass

        pass


class GearmanLogReader(object):
    log = []

    sender = 'gearman'

    def __init__(self, reader):
        GearmanLogReader.log = reader.tail(10000)

    def get_summary(self, records):
        for record in records:
            if 'queues' in record['params']:
                return record

    def get_tasks_stats(self, records):
        stats = {}
        for record in records:
            if 'task' not in record['params']:
                continue

            if record['params']['task'] not in stats:
                stats[record['params']['task']] = record

        return stats


    def get_records_for(self, gearman):

        gearman_signature = 'host=%s,port=%s' % (gearman.server.host, gearman.port)

        records = []

        for entry in GearmanLogReader.log:
            if entry.sender != GearmanLogReader.sender:
                continue

            params = dict(zip(map(lambda i: i.strip(':'), entry.message.split()[::2]), entry.message.split()[1::2]))

            if params['from'].rstrip(']').lstrip('[') == gearman_signature:
                records.append({'time': entry.time, 'level': entry.level, 'message': entry.message, 'params': params})

        summary = self.get_summary(records)

        tasks_stats = self.get_tasks_stats(records)

        return {'summary': summary, 'stats': tasks_stats }



class SupervisorLogReader(object):
    log = []

    sender = 'supervisor'

    def __init__(self, reader):
        SupervisorLogReader.log = reader.tail(10000)
#        print [ i.message for i in SupervisorLogReader.log]

    def get_records_for(self, supervisor):

        supervisor_signature = 'host=%s,port=%s' % (supervisor.server.host, supervisor.port)

        records = []

        for entry in SupervisorLogReader.log:
            if entry.sender != SupervisorLogReader.sender:
                continue

            params = dict(zip(map(lambda i: i.strip(':'), entry.message.split()[::2]), entry.message.split()[1::2]))

            if params['from'].rstrip(']').lstrip('[') == supervisor_signature:
                records.append({'time': entry.time, 'level': entry.level, 'message': entry.message, 'params': params})

        return records

class ProcessLogReader(object):
    log = []

    sender = 'process'

    def __init__(self, reader):
        ProcessLogReader.log = reader.tail(10000)

    def get_records(self):

#       USERNAME: root
#       MEM: [info=meminfo(rss=7188480, vms=38723584),percent=0.227480706266]
#       PID: 3678
#       CMDLINE: pythonenv_stub/workers/reverse.py
#       RUNNING: True
#       UIDS: user(real=0, effective=0, saved=0)
#       FROM: root@127.0.0.1
#       NAME: python
#       CREATED: 1312027920.21
#       PPID: 902
#       CPU: [percent=0.0,times=cputimes(user=0.19, system=0.02)]

        records = {}

        for entry in ProcessLogReader.log:
            if entry.sender != ProcessLogReader.sender:
                continue

#            params = dict(zip(map(lambda i: i.strip(':'), entry.message.split()[::2]), entry.message.split()[1::2]))

            params = {}

            m = '- %s -' % entry.message
            try:
                reg = re.compile(r' pid\: ([\d]+) ')
                params['pid'] = reg.findall(m).pop()

                reg = re.compile(r' from\: ([^:]+) ')
                params['from'] = reg.findall(m).pop()
            except Exception, e:
                continue

            try:
                reg = re.compile(r' mem\: \[([^:\]]+)\]')
                res = reg.findall(m).pop()
                reg = re.compile(r'percent=([\.\d]+)')
                params['mem'] = reg.findall(res).pop()
            except Exception, e:
                params['mem'] = 0

            try:
                reg = re.compile(r' cpu\: \[([^:]+)\]')
                res = reg.findall(m).pop()
                reg = re.compile(r'percent=([\.\d]+)')
                params['cpu'] = reg.findall(res).pop()
            except Exception, e:
                params['cpu'] = 0


            key = params['from'] + '_' + params['pid']
            if key not in records:
                records[key] = {'pid': params['pid'],
                                'time': entry.time, 'level': entry.level, 'message': entry.message,
                                'cpu':round( float(params['cpu'])), 'mem': round( float(params['mem']))}

        return records

