from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^all/$', views.EventListView.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', views.EventDetailView.as_view()),
]
