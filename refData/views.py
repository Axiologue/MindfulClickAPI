from refData.models import Article
from refData.serializers import ArticleSerializer

from rest_framework import generics
from django.db.models import Count

class ArticleNoCrossView(generics.ListAPIView):
    queryset = Article.objects.annotate(c=Count('data')).filter(c=0)
    serializer_class = ArticleSerializer
