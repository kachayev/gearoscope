from django.db import models

class LastRevisionManager(models.Manager):
    '''
    Return QuerySet object with changed order
    and command for returning only values, not objects.
    Operating with revision values will save application
    from bugs during trying to resave existen object
    '''
    def get_query_set(self):
        return super(LastRevisionManager, self).get_query_set().order_by('-time').values()

