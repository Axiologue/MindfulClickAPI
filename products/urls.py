from django.conf.urls import url

from . import views
from profile.views import ProductFetchView

urlpatterns = [
    url(r'^companies/all/$', views.AllCompaniesView.as_view()),
    url(r'^companies/(?P<pk>\d+)/$', views.SingleCompanyView.as_view()),
    url(r'^products/(?P<pk>\d+)/$', views.SingleProductView.as_view()),
    url(r'^products/list/$', views.ProductListView.as_view()),
    url(r'^products/fetch/$', ProductFetchView.as_view()),
    url(r'^products/new/$', views.ProductNewView.as_view()),
]
