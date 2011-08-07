from django.db import models

class LastRevisionManager(models.Manager):
    def get_query_set(self):
        return super(LastRevisionManager, self).get_query_set().order_by('-time').values()

