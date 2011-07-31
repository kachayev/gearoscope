from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson
from models import *
from scoper.models import Server, Supervisor, Gearman
from monitor.reader import Reader
from django.conf import settings
import logging

def index(request):

#    workers = Workers().get_workers()
    servers = Server.objects.all()
    supervisords = Supervisor.objects.all()
    gearmans = Gearman.objects.all()

    reader = Reader(settings.SONAR_LOG_FILE)
    gearman_log = GearmanLogReader(reader)
    params = {}
    params['gearmans'] = {}
    for gearman in Gearman.objects.all():
        params['gearmans'][gearman.crc_it()] = gearman_log.get_records_for(gearman)

    for item in params['gearmans'].itervalues():
        for queue in item['stats']:
            logging.error(queue)

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

    response['supervisords'] = {}

    super_log = SupervisorLogReader(reader)

    for supervisor in Supervisor.objects.all():
        response['supervisords'][supervisor.crc_it()] = super_log.get_records_for(supervisor)


#    response['processes'] = Process().getData()

    gearman_log = GearmanLogReader(reader)

    response['gearmans'] = {}
    for gearman in Gearman.objects.all():
        response['gearmans'][gearman.crc_it()] = gearman_log.get_records_for(gearman)


    response['workers'] = {}

    for worker in Workers().get_workers():
        response['workers'][worker['id']] = Workers().get_data(worker['id'])

#    except Exception, e :
#        response['result'] = 'error'
#        logging.error(e.message)

    json = simplejson.dumps(response)

    return HttpResponse(json, mimetype='application/json', content_type='json')

