from django.db import models

class Revision(models.Model):
    '''
    Save in database history of changes in servers and workers configurations

    New revision will be created and saved to database on each modification of
    monitoring relative database instances (configuration, server etc). This
    functionality will be automaticaly handled by post_save signals in
    scope model module
    '''
    CONFIG     = 1
    SERVER     = 2
    SUPERVISOR = 3
    WORKER     = 4
    GEARMAN    = 5
    QUEUE      = 6
    AGENT      = 7
    POOL       = 8

    MODIFY_CHOICES = (
        (CONFIG,     u'Configuration'),
        (SERVER,     u'Server'),
        (SUPERVISOR, u'Supervisor'),
        (WORKER,     u'Worker'),
        (GEARMAN,    u'Gearman'),
        (QUEUE,      u'Queue'),
        (AGENT,      u'Agent'),
        (POOL,       u'Pool'),
    )

    # Determing parm of application configuration,
    # which was modified during last database operation
    modification = models.IntegerField(default=CONFIG, choices=MODIFY_CHOICES)

    # Modification time, will be set automaticly to the current time of revision creating
    time = models.DateTimeField(auto_now_add=True)

