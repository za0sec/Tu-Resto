from django.conf import settings
from django.conf.urls.static import static
from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host(r'api', 'apps.api.urls', name='api'), 
    host(r'media', 'apps.media.urls', name='media'),
    host(r'wpp', 'apps.wpp.urls', name='wpp')
)