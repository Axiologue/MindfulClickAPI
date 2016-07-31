from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^companies/all/$', views.AllCompaniesView.as_view()),
    url(r'^companies/(?P<pk>\d+)/$', views.SingleCompanyView.as_view()),
    url(r'^companies/(?P<name>[\w\s-]+)/$', views.SingleByNameCompanyView.as_view()),
    url(r'^products/(?P<pk>\d+)/$', views.SingleProductView.as_view()),
    url(r'^products/list/$', views.ProductListView.as_view()),
    url(r'^products/new/$', views.ProductNewView.as_view()),
]
