from django.conf.urls import url
from refData import views

urlpatterns = [
    url(r'^articles/$',views.ArticleNoCrossView.as_view()),
]