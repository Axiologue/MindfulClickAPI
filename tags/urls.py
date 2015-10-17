from django.conf.urls import url
from tags import views

urlpatterns = [
    url(r'^formMeta/',views.FormMetaView.as_view()),
    url(r'^tags/new/$',views.NewEthicsTagView.as_view()),
    url(r'^tags/(?P<pk>\d+)/$',views.UpdateEthicsTagView.as_view()),
    url(r'^tag-types/new/$',views.NewEthicsTypeView.as_view()),
]
