from django.conf.urls import url

from profile import views

urlpatterns = [
    url(r'^prefs/all/$',views.EthicsProfileView.as_view()),
    url(r'^prefs/(?P<pk>\d+)/$',views.PrefUpdateView.as_view()),
    url(r'^scores/company/(?P<pk>\d+)/$',views.CompanyScoreView.as_view()),
    url(r'^scores/product/(?P<pk>\d+)/$',views.ProductScoreView.as_view()),
    url(r'^question/all/$',views.QuestionListView.as_view()),
    url(r'^question/all-answers/$',views.QuestionWithAnswersListView.as_view()),
    url(r'^question/new/$',views.NewQuestionView.as_view()),
    url(r'^question/answers/(?P<pk>\d+)/$',views.QuestionAnswersView.as_view()),
    url(r'^question/answers/set/$',views.SetAnswersView.as_view()),
    url(r'^question/answer/(?P<pk>\d+)/new/$',views.NewAnswerView.as_view()),
    url(r'^question/answer/(?P<pk>\d+)/updateAll/$',views.UpdateAnswersView.as_view()),
    url(r'^meta/answered/$',views.UserAnsweredView.as_view()),
]

