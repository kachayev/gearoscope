from django.conf.urls.defaults import patterns, url
from views import *

urlpatterns = patterns('',
    # Example:
    url(r'^$', index, name='home'),
    
    url(r'dashboard', dashboard, name='dashboard'),

)
