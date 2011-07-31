import binascii
from django.db import models
from django.contrib import admin
import logging

class Server(models.Model):
    '''
    Server node instance

    Should be allocated by host and other SSH access params (user, password, port etc). SSH connection
    is necessary for working with PS on remote machine (this will be necessary
    to get information about each worker status). Host should be valid IP address or named host,
    which could be resolved by network facilities.

    Server model will be used from other models to create relation between process
    and supervisors to concrete physical server node
    '''
    # Main params (required)
    host = models.CharField(max_length='255', default='localhost', primary_key=True)
    name = models.CharField(max_length='255', default='localhost',
                            unique=True, help_text='Any name which will simplify server identity')

    # Additional params (non-required)
    user     = models.CharField(default='root', max_length='64',
                                help_text='Username for SSH access to server')
    password = models.CharField(blank=True, null=True, max_length='255',
                                help_text='Password for SSH access to server')
    ssh_key  = models.TextField(blank=True, null=True,
                                verbose_name='SSH key',
                                help_text='Absolute path to SSH private key (in most cases OS will find it automaticaly)')
    ssh_port = models.PositiveIntegerField(default=22, verbose_name='SSH port')

    def __unicode__(self):
        '''Clean human-understanding string represantation for server node'''
        return '%s (%s)' % (self.name, self.host)

class ServerAdmin(admin.ModelAdmin):
    '''
    Params for server nodes managment via administrative panel

    Override params for fieldsets value in order to create two blocks:
    # general params (required)
    # ssh connection params (which should be edited just in case of non-standard OS params)

    In future we can add here inlined models for workers and gearman nodes
    to give user more flexible way to add per-server items
    '''
    fieldsets = (
        (None, {
            'fields': ('host', 'name')
        }),
        ('SSH connection options', {
            'description': 'Leave default values if you do not know exactly what you are doing',
            'fields': ('user', 'password', 'ssh_key', 'ssh_port')
        }),
    )

# Register server node manage-place in administration panel
admin.site.register(Server, ServerAdmin)

class ServerLogReader(object):
    log = []
    
    def __init__(self, reader):
        ServerLogReader.log = reader.tail(100)

    def get_records_for(self, server):

        for entry in ServerLogReader.log:
            logging.error(entry)
            pass

        pass



class Gearman(models.Model):
    '''
    Gearman node instance

    Gearman node will be used in code for providing params to GearmanAdminClient
    (blocking socket client). To establish connection, we should provide server's host
    (will be taked from foreign object Server) and port (remote socket). According to
    protocol specification, default port is 4730, but it can be change via gearman daemon
    running params.

    More information about protocol specification you can find in oficial Gearman documentation:
        http://gearman.org/index.php?id=protocol
    or in documentation to Python client:
        http://packages.python.org/gearman/
    '''
    server = models.ForeignKey(Server)
    port = models.PositiveIntegerField(default=4730)

    def __unicode__(self):
        '''Clean human-understanding string represantation for gearman node'''
        return '%s:%s' % (self.server.host, self.port)

class GearmanAdmin(admin.ModelAdmin):
    '''Params for gearman nodes managment via administrative panel'''
    pass

# Register gearman node manager in administration panel
admin.site.register(Gearman, GearmanAdmin)

class Supervisor(models.Model):
    '''
    Supervisor daemon instance

    Supervisor model objects will be used in monitorin agents, which will
    use XML-RPC connection for retrieving information about running processes.
    To avoid problems with "Connection refuse" error, please check that:
    - XML-RPC is switched on
    - supervisor configuration contains inet_http_server section without direct settings for IP

    More information about supervisor configuration you can find in official documentation:
    http://supervisord.org/configuration.html
    '''
    server = models.ForeignKey(Server)
    port = models.PositiveIntegerField(default=9001)

    def __unicode__(self):
        '''Clean human-understanding string represantation for supervisor daemon'''
        return '%s:%s' % (self.server.host, self.port)

    def crc_it(self):
        return binascii.crc32(self.__unicode__())

class SupervisorAdmin(admin.ModelAdmin):
    '''Params for supervisor daemons managment via administrative panel'''
    pass

# Register gearman node manager in administration panel
admin.site.register(Supervisor, SupervisorAdmin)

class SupervisorLogReader(object):
    log = []

    sender = 'supervisor'

    def __init__(self, reader):
        SupervisorLogReader.log = reader.tail(100)

    def get_records_for(self, supervisor):

        supervisor_signature = 'host=%s,port=%s' % (supervisor.server.host, supervisor.port)

        records = []

        for entry in SupervisorLogReader.log:
            logging.error(entry.sender)
            logging.error(SupervisorLogReader.sender)
            if entry.sender != SupervisorLogReader.sender:
                continue
                
            params = dict(zip(map(lambda i: i.strip(':'), entry.message.split()[::2]), entry.message.split()[1::2]))
            logging.error(params)
            logging.error(supervisor_signature)
            logging.error(params['from'].rstrip(']').lstrip('['))

            if params['from'].rstrip(']').lstrip('[') == supervisor_signature:
                logging.error('found our wisard')
                records.append({'time': entry.time, 'level': entry.level, 'message': entry.message, 'params': params})

        records.sort(key=lambda x: x['time'])

        return records

