from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'recent/$', views.RecentInfoView.as_view(), name="recent-info"),
]
