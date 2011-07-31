from django.db import models

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
    host = models.CharField(max_length='256', default='localhost', primary_key=True)
    name = models.CharField(max_length='256', default='localhost',
                            unique=True, help_text='Any name which will simplify server identity')

    # Additional params (non-required)
    user = models.CharField(default='root', help_text='Username for SSH access to server', empty=True)
    password = models.CharField(empty=True,
                                help_text='Password for SSH access to server')
    ssh_key = models.TextField(empty=True,
                               help_text='Absolute path to SSH private key (in most cases OS will find it automaticaly)')
    ssh_port = models.PositiveIntegerField(default=22, empty=True)

    def __unicode__(self):
        '''Clean human-understanding string represantation for server node'''
        return '%s (%s)' % (self.name, self.host)

