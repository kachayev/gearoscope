from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson
from models import *
import logging

def index(request):

    workers = Workers().get_workers()
    servers = Server().get_servers()
    logging.error(servers)
    return render_to_response('dashboard/index.html', locals())

def dashboard(request):
    response = {'result': 'ok'}

#    try:
    response['servers'] = Server().get_data()
    response['supervisords'] = Supervisor().getData()
    response['processes'] = Process().getData()
    response['workers'] = {}

    for worker in Workers().get_workers():
        response['workers'][worker['id']] = Workers().get_data(worker['id'])
            
#    except Exception, e :
#        response['result'] = 'error'
#        logging.error(e.message)

    json = simplejson.dumps(response)
    
    return HttpResponse(json, mimetype='application/json', content_type='json')

