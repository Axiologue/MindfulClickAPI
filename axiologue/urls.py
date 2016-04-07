"""cross URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url('^$', views.LandingView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^articles/', include('references.urls', namespace='articles')),
    url(r'^references/', include('references.urls', namespace='articles')),
    url(r'^tags/', include('tags.urls', namespace='tags')),
    url(r'^profile/', include('profile.urls', namespace='profile')),
    url(r'^products/', include('products.urls', namespace='products')),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^landing/', include('landing.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
