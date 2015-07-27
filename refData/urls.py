from django.conf.urls import url
from refData import views

urlpatterns = [
    url(r'^formMeta/',views.FormMetaView.as_view()),
    url(r'^articles/all/$',views.ArticleNoCrossView.as_view()),
    url(r'^articles/new/$',views.NewArticleView.as_view()),
    url(r'^articles/(?P<pk>\d+)/$',views.UpdateArticleView.as_view()),
    url(r'^cross/list/$',views.ArticleWithCrossView.as_view()),
    url(r'^cross/new/$',views.NewCrossView.as_view()),
    url(r'^cross/(?P<pk>\d+)/$',views.UpdateCrossView.as_view()),
]