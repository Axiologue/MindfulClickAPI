from refData.models import Article, Product, EthicsCategory, Company, CrossReference
from refData.serializers import ArticleSerializer, CrossByArticle, ArticleNoIDSerializer, ProductSerializer, \
        EthicsSerializer, CompanySerializer, CrossSerializer, CrossCreateSerializer

from drf_multiple_model.views import MultipleModelAPIView

from rest_framework import generics, mixins
from django.db.models import Count

class ArticleNoCrossView(generics.ListAPIView):
    queryset = Article.objects.annotate(c=Count('data')).filter(c=0)
    serializer_class = ArticleSerializer


class ArticleWithCrossView(MultipleModelAPIView):
    queryList = [
        (Article.objects.prefetch_related('data__company','data__subcategory').annotate(c=Count('data')).filter(c__gte=1), 
            CrossByArticle),
        (EthicsCategory.objects.prefetch_related('subcategories').all(),EthicsSerializer),
        (Company.objects.all(),CompanySerializer)
    ]


class UpdateArticleView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ArticleSerializer
    queryset= Article.objects.all()

class NewArticleView(generics.CreateAPIView):
    serializer_class = ArticleSerializer
    queryset= Article.objects.all()

class NewCrossView(generics.CreateAPIView):
    queryset = CrossReference.objects.all()
    serializer_class = CrossCreateSerializer