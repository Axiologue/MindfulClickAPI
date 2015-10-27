from django.conf.urls import url

from profile import views

urlpatterns = [
    url(r'^prefs/all/$',views.EthicsProfileView.as_view()),
    url(r'^prefs/(?P<pk>\d+)/$',views.PrefUpdateView.as_view()),
    url(r'^scores/company/(?P<pk>\d+)/$',views.CompanyScoreView.as_view()),
]

