from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson
from models import *
import logging

def index(request):

    return render_to_response('dashboard/index.html')

def dashboard(request):
    response = {'result': 'ok'}

    try:
        response['servers'] = Server().getData()
        response['supervisords'] = Supervisor().getData()
        response['processes'] = Process().getData()

    except Exception, e :
        response['result'] = 'error'
        logging.error(e.message)

    json = simplejson.dumps(response)
    
    return HttpResponse(json, mimetype='application/json', content_type='json')

