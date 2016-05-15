from django.conf.urls import url, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    url(r'^category/list/$', views.CategoryListView.as_view()),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryDetailView.as_view()),
    url(r'^threads/(?P<pk>[0-9]+)/$', views.ThreadListView.as_view()),
    url(r'^threads/new/$', views.ThreadNewView.as_view()),
    url(r'^posts/(?P<pk>[0-9]+)/$', views.PostListView.as_view()),
]
