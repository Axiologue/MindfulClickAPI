from django.conf.urls import url
from refData import views

urlpatterns = [
    url(r'^articles/$',views.ArticleNoCrossView.as_view()),
    url(r'^articles/new/$',views.NewArticleView.as_view()),
    url(r'^articles/update/(?P<pk>\d+)/$',views.UpdateArticleView.as_view()),
    url(r'^articles/delete/(?P<pk>\d+)/$',views.DeleteArticleView.as_view()),
    url(r'^cross-list/$',views.ArticleWithCrossView.as_view()),
]