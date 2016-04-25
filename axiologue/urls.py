from django.conf.urls import include, url
from django.contrib import admin

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
    url(r'^search/', include('search.urls')),
    url(r'^forum/', include('forum.urls', namespace='forum')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^', include('django.contrib.auth.urls')),
]
