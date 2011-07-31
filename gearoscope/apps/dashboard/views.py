from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson
from models import *
from scoper.models import Server, Supervisor, Gearman
from monitor.reader import Reader
from django.conf import settings
import logging

def index(request):

    servers = Server.objects.all()
    supervisords = Supervisor.objects.all()
    gearmans = Gearman.objects.all()

    reader = Reader(settings.SONAR_LOG_FILE)
    gearman_log = GearmanLogReader(reader)
    params = {}
    params['gearmans'] = {}
    for gearman in Gearman.objects.all():
        params['gearmans'][gearman.crc] = gearman_log.get_records_for(gearman)

    for item in params['gearmans'].itervalues():
        for queue in item['stats']:
            logging.error(queue)

    proceses = get_processes(reader)

    workers = get_workers(get_supervisords(reader), proceses)

    return render_to_response('dashboard/index.html', locals())

def dashboard(request):
    response = {'result': 'ok'}

#    try:
    reader = Reader(settings.SONAR_LOG_FILE)
    
    response['servers'] = []
    server_log = ServerLogReader(reader)
    servers = Server.objects.all()

#    for server in servers:
#        server['records'] = server_log.get_records_for(server)
#        response['servers'].append(server)

    response['supervisords'] = get_supervisords(reader)

    response['processes'] = get_processes(reader)

    response['workers'] = get_workers(response['supervisords'], response['processes'])

    gearman_log = GearmanLogReader(reader)

    response['gearmans'] = {}
    for gearman in Gearman.objects.all():
        response['gearmans'][gearman.crc] = gearman_log.get_records_for(gearman)

    json = simplejson.dumps(response)

    return HttpResponse(json, mimetype='application/json', content_type='json')

def get_supervisords(reader):
    supervisords = {}

    super_log = SupervisorLogReader(reader)

    for supervisor in Supervisor.objects.all():
        supervisords[supervisor.crc] = super_log.get_records_for(supervisor)

    return supervisords


def get_processes(reader):

    log = ProcessLogReader(reader)
    return log.get_records()

def get_workers(supervisords, processes):
    workers = {}

    for proc_id, proc in processes.iteritems():
        for sup in supervisords.itervalues():
            for sup_proc in sup:

                if sup_proc['params']['pid'] == proc['pid']:
                    key = sup_proc['params']['name']
                    if key not in workers:
                        workers[key] = {}
                    workers[key][proc_id] = proc

    return workers
