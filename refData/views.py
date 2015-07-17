from refData.models import Article, Product, EthicsCategory, Company, CrossReference
from refData.serializers import ArticleSerializer, CrossByArticle, ArticleNoIDSerializer, ProductSerializer, \
        EthicsSerializer, CompanySerializer, CrossSerializer, CrossCreateSerializer

from drf_multiple_model.views import MultipleModelAPIView

from rest_framework import generics
from django.db.models import Count

class ArticleNoCrossView(MultipleModelAPIView):
    queryList = [
        (Article.objects.annotate(c=Count('data')).filter(c=0),ArticleSerializer),
        (EthicsCategory.objects.all(),EthicsSerializer),
        (Company.objects.all(),CompanySerializer)
    ]


class ArticleWithCrossView(generics.ListAPIView):
    queryset = Article.objects.annotate(c=Count('data')).filter(c__gte=1)
    serializer_class = CrossByArticle

class NewArticleView(generics.CreateAPIView):
    serializer_class = ArticleNoIDSerializer

class UpdateArticleView(generics.UpdateAPIView):
    serializer_class = ArticleSerializer
    queryset= Article.objects.all()

class DeleteArticleView(generics.DestroyAPIView):
    serializer_class = ArticleSerializer
    queryset= Article.objects.all()

class NewCrossView(generics.CreateAPIView):
    queryset = CrossReference.objects.all()
    serializer_class = CrossCreateSerializer