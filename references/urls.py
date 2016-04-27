from django.conf.urls import url

from . import views

urlpatterns = [
    # Above is outdated endpoints: below are the new and improved ones
    url(r'^list/$', views.ReferenceWithTagsView.as_view()),
    url(r'^untagged/$', views.ReferenceNoTagView.as_view()),
    url(r'^tagged/$', views.ReferenceWithCrossView.as_view()),
    url(r'^tagged/company/(?P<pk>\d+)/$', views.ReferenceWithCrossByCompanyView.as_view()),
    url(r'^new/$', views.NewReferenceView.as_view()),
    url(r'^(?P<pk>\d+)/$', views.UpdateReferenceView.as_view()),
    url(r'^noData/$', views.ReferenceNoDataView.as_view()),
]
