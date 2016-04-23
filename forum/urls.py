from django.conf.urls import url, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns



urlpatterns = [
    url(r'^$', views.thread_list, name='thread_list'),
    url(r'^thread/new/$', views.thread_new, name='thread_new'), 
    url(r'^thread/(?P<pk>\d+)/$', views.thread_detail, name='thread_detail'),
    url(r'^post/new/(?P<pk>\d+)/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^api/thread/$', views.APIThreadList.as_view()),
    url(r'^api/thread/(?P<pk>[0-9]+)/$', views.APIThreadDetail.as_view()),
    url(r'^api/post/$', views.APIPostList.as_view()),
    url(r'^api/post/(?P<pk>[0-9]+)/$', views.APIPostDetail.as_view()),
    #url(r'^api/users/$', views.APIUserList.as_view()),
    #url(r'^api/users/(?P<pk>[0-9]+)/$', views.APIUserDetail.as_view()),
       
]

urlpatterns += [
    url(r'^api/auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]

urlpatterns = format_suffix_patterns(urlpatterns)

