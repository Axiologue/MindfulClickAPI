from django.conf.urls import url
from refData import views

urlpatterns = [
    url(r'^formMeta/',views.FormMetaView.as_view()),
    url(r'^articles/untagged/$',views.ArticleNoTagView.as_view()),
    url(r'^articles/tagged/$',views.ArticleWithCrossView.as_view()),
    url(r'^articles/new/$',views.NewArticleView.as_view()),
    url(r'^articles/(?P<pk>\d+)/$',views.UpdateArticleView.as_view()),
    url(r'^tags/new/$',views.NewTagView.as_view()),
    url(r'^tags/(?P<pk>\d+)/$',views.UpdateTagView.as_view()),
]