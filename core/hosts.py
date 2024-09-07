from django.conf import settings
from django.conf.urls.static import static
from django_hosts import patterns, host
host_patterns = patterns(
    '',
    host(r'api', 'apps.api.urls', name='api')
)

if settings.DEBUG:
    # Servir archivos de media y estáticos bajo el subdominio 'api'
    urlpatterns = [
        # Rutas para los archivos de media
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)