from django.db import models
from django.contrib import admin

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

class SupervisorAdmin(admin.ModelAdmin):
    '''Params for supervisor daemons managment via administrative panel'''
    pass

# Register supervisor node manager in administration panel
admin.site.register(Supervisor, SupervisorAdmin)

class Worker(models.Model):
    '''
    Worker process instance

    Stop signal params will be used by supervisor during start/restart calls. What signal to use
    in order to stop execution of you process in best way dependce on process implementation. Full
    list of signal and more information about it, you can find here:
    http://www.cs.pitt.edu/~alanjawi/cs449/code/shell/UnixSignals.htm
    '''
    SIGHUP  = 1
    SIGINT  = 2
    SIGQUIT = 3
    SIGKILL = 9
    SIGTERM = 15
    SIGUSR1 = 16
    SIGUSR2 = 17

    SIGNAL_CHOICES = (
        (SIGHUP,  u'HUP'),
        (SIGINT,  u'INT'),
        (SIGQUIT, u'QUIT'),
        (SIGKILL, u'KILL'),
        (SIGTERM, u'TERM'),
        (SIGUSR1, u'USR1'),
        (SIGUSR2, u'USR2'),
    )

    # Identity required params
    supervisor = models.ForeignKey(Supervisor)
    name = models.CharField(max_length=70)

    # General required params
    command = models.CharField(max_length=255)
    process_name = models.CharField(max_length=70)
    numprocs = models.PositiveSmallIntegerField(default=1, blank=True, null=True)

    # Field which describe process running params and env variables
    directory = models.CharField(max_length=255, default='/', blank=True, null=True)
    umask = models.CharField(max_length=4, default='022', blank=True, null=True)
    user = models.CharField(max_length=255, blank=True, null=True)
    priority = models.PositiveIntegerField(default=999, blank=True, null=True)
    environment = models.CharField(max_length=255, default='', blank=True)

    # Param for starting and restarting process
    autostart = models.BooleanField(default=True)
    autorestart = models.BooleanField(default=True)
    startsecs = models.PositiveSmallIntegerField(default=10)
    startretries = models.PositiveSmallIntegerField(default=3)
    stopwaitsecs = models.PositivIntegerField(default=10)

    # Exit params (should tell supervisor how to stop and restart process)
    # and what stop suggest as normal one (non-error)
    exitcodes = models.CommaSeparatedIntegerField(default='0,2')
    stopsignal = models.IntegerField(default=SIGTERM, choices=SIGNAL_CHOICES)

    # Params for logging of proces STDOUT and STDERR
    # Useful in order if we want to get log tails via XML-RPC protocol
    redirect_stderr = models.BooleanField(default=False)
    stdout_logfile = models.CharField(max_length=255)
    stdout_logfile_maxbytes = models.PositiveIntegerField(default=1)
    stdout_logfile_backups = models.PositiveIntegerField(default=10)
    stdout_capture_maxbytes = models.PositiveIntegerField(default=1)
    stderr_logfile = models.CharField(max_length=50, blank=True)
    stderr_logfile_maxbytes = models.PositiveIntegerField(default=1)
    stderr_logfile_backups = models.PositiveIntegerField(default=10)
    stderr_capture_maxbytes = models.PositiveIntegerField(default=1)

    def __unicode__(self):
        '''
        Clean human-understanding string represantation for worker process
        Contains process name and full string representation for supervisor model
        object (see below for more details)
        '''
        return '%s @ %s' % (self.name, str(self.supervisor))

class WorkerAdmin(admin.ModelAdmin):
    '''Params for workers managment via administrative panel'''
    pass

# Register workers manager in administration panel
admin.site.register(Worker, WorkerAdmin)

