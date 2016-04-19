from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'posts/all/$', views.AllPostsView.as_view(), name="all-posts"),
    url(r'posts/recent/$', views.RecentPostsView.as_view(), name='recent-posts'),
    url(r'posts/(?P<title_url>[\w-]+)/$', views.PostView.as_view(), name='post')
]
