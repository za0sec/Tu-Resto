from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host(r'api', 'apps.api.urls', name='api')
)
