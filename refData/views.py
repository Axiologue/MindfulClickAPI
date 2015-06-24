from refData.models import Article
from refData.serializers import ArticleSerializer, CrossByArticle, ArticleNoIDSerializer

from rest_framework import generics
from django.db.models import Count

class ArticleNoCrossView(generics.ListAPIView):
    queryset = Article.objects.annotate(c=Count('data')).filter(c=0)
    serializer_class = ArticleSerializer

class ArticleWithCrossView(generics.ListAPIView):
    queryset = Article.objects.annotate(c=Count('data')).filter(c__gte=1)
    serializer_class = CrossByArticle

class NewArticleView(generics.CreateAPIView):
    serializer_class = ArticleNoIDSerializer