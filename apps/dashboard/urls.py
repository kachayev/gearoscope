from django.conf.urls.defaults import patterns, url
from views import index

urlpatterns = patterns('',
    # Example:
    url(r'^$', index, name='home'),

)
