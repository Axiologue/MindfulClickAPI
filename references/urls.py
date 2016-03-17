from django.conf.urls import url

from . import views
from profile.views import ProductFetchView

urlpatterns = [
    url(r'^articles/untagged/$',views.ArticleNoTagView.as_view()),
    url(r'^articles/tagged/$',views.ArticleWithCrossView.as_view()),
    url(r'^articles/tagged/company/(?P<pk>\d+)/$',views.ArticleWithCrossByCompanyView.as_view()),
    url(r'^articles/new/$',views.NewArticleView.as_view()),
    url(r'^articles/(?P<pk>\d+)/$',views.UpdateArticleView.as_view()),
    url(r'^articles/noData/$',views.ArticleNoDataView.as_view()),
    url(r'^companies/all/$',views.AllCompaniesView.as_view()),
    url(r'^companies/(?P<pk>\d+)/$',views.SingleCompanyView.as_view()),
    url(r'^products/(?P<pk>\d+)/$',views.SingleProductView.as_view()),
    url(r'^products/list/$',views.ProductListView.as_view()),
    url(r'^products/fetch/$',ProductFetchView.as_view()),
    url(r'^products/new/$',views.ProductNewView.as_view()),
]
