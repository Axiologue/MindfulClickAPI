from refData.models import Article, Product, EthicsSubCategory, Company, CrossReference
from refData.serializers import ArticleSerializer, CrossByArticle, ArticleNoIDSerializer, ProductSerializer, \
        EthicsSubSerializer, CompanySerializer, CrossSerializer, CrossCreateSerializer, CrossUpdateSerializer

from drf_multiple_model.views import MultipleModelAPIView

from rest_framework import generics, mixins
from django.db.models import Count

class ArticleNoCrossView(generics.ListAPIView):
    queryset = Article.objects.annotate(c=Count('data')).filter(c=0)
    serializer_class = ArticleSerializer


class ArticleWithCrossView(generics.ListAPIView):
    queryset= Article.objects.prefetch_related(
        'data__company',
        'data__subcategory'
        ).annotate(c=Count('data')).filter(c__gte=1)
    serializer_class = CrossByArticle;

class UpdateArticleView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ArticleSerializer
    queryset= Article.objects.all()

class NewArticleView(generics.CreateAPIView):
    serializer_class = ArticleSerializer
    queryset= Article.objects.all()

class NewCrossView(generics.CreateAPIView):
    queryset = CrossReference.objects.all()
    serializer_class = CrossCreateSerializer

class FormMetaView(MultipleModelAPIView):
    queryList = [
        (Company.objects.all().order_by('name'),CompanySerializer),
        (EthicsSubCategory.objects.all(),EthicsSubSerializer)
    ]

class UpdateCrossView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CrossUpdateSerializer
    queryset= CrossReference.objects.all()