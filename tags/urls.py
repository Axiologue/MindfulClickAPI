from django.conf.urls import url
from tags import views

urlpatterns = [
    url(r'^formMeta/',views.FormMetaView.as_view()),
    url(r'^etags/new/$',views.NewEthicsTagView.as_view()),
    url(r'^etags/(?P<pk>\d+)/$',views.UpdateEthicsTagView.as_view()),
    url(r'^etypes/new/$',views.NewEthicsTypeView.as_view()),
    url(r'^mtags/new/$',views.NoRelDataView.as_view()),
    url(r'^mtags/(?P<pk>\d+)/$',views.UpdateMetaTagView.as_view())
]
