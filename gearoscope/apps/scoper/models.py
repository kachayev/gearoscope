from django.db import models
from django.contrib import admin

class Server(models.Model):
    '''
    Server node instance

    Should be allocated by host and other SSH access params (user, password, port etc). SSH connection
    is necessary for working with PS on remote machine (this will be necessary
    to get information about each worker status)

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
                                help_text='Absolute path to SSH private key (in most cases OS will find it automaticaly)')
    ssh_port = models.PositiveIntegerField(default=22)

    def __unicode__(self):
        '''Clean human-understanding string represantation for server node'''
        return '%s (%s)' % (self.name, self.host)

class ServerAdmin(admin.ModelAdmin):
    '''Params for server nodes managment via administrative panel'''
    fieldsets = (
        (None, {
            'fields': ('host', 'name')
        }),
        ('SSH connection options', {
            'fields': ('user', 'password', 'ssh_key', 'ssh_port')
        }),
    )

admin.site.register(Server, ServerAdmin)

