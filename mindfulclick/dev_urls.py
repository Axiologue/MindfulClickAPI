import debug_toolbar
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static

from .urls import urlpatterns


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls)),]
