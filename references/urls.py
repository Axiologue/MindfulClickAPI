from django.conf.urls import url

from . import views
from products import views as productViews
from profile.views import ProductFetchView

urlpatterns = [
    url(r'^articles/untagged/$', views.ReferenceNoTagView.as_view()),
    url(r'^articles/tagged/$', views.ReferenceWithCrossView.as_view()),
    url(r'^articles/tagged/company/(?P<pk>\d+)/$', views.ReferenceWithCrossByCompanyView.as_view()),
    url(r'^articles/new/$', views.NewReferenceView.as_view()),
    url(r'^articles/(?P<pk>\d+)/$', views.UpdateReferenceView.as_view()),
    url(r'^articles/noData/$', views.ReferenceNoDataView.as_view()),
    url(r'^companies/all/$', productViews.AllCompaniesView.as_view()),
    url(r'^companies/(?P<pk>\d+)/$', productViews.SingleCompanyView.as_view()),
    url(r'^products/(?P<pk>\d+)/$', productViews.SingleProductView.as_view()),
    url(r'^products/list/$', productViews.ProductListView.as_view()),
    url(r'^products/fetch/$', ProductFetchView.as_view()),
    url(r'^products/new/$', productViews.ProductNewView.as_view()),
    # Abvoe is outdated endpoints: below are the new and improved ones
    url(r'^untagged/$', views.ReferenceNoTagView.as_view()),
    url(r'^tagged/$', views.ReferenceWithCrossView.as_view()),
    url(r'^tagged/company/(?P<pk>\d+)/$', views.ReferenceWithCrossByCompanyView.as_view()),
    url(r'^new/$', views.NewReferenceView.as_view()),
    url(r'^(?P<pk>\d+)/$', views.UpdateReferenceView.as_view()),
    url(r'^noData/$', views.ReferenceNoDataView.as_view()),
]
