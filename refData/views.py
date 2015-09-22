from refData.models import Article, Product, EthicsSubCategory, Company, Tag, TagType
from refData.serializers import ArticleSerializer, ProductSerializer, \
        EthicsSubSerializer, CompanySerializer, TagsByArticle, TagChangeSerializer, TagSerializer, \
        TagTypeSerializer, TagTypeUpdateSerializer

from drf_multiple_model.views import MultipleModelAPIView

from rest_framework import generics, mixins
from django.db.models import Count

class ArticleNoTagView(generics.ListAPIView):
    queryset = Article.objects.annotate(c=Count('tags')).filter(c=0)
    serializer_class = ArticleSerializer


class ArticleWithCrossView(generics.ListAPIView):
    queryset= Article.objects.prefetch_related(
        'tags__company',
        'tags__tag_type'
        ).annotate(c=Count('tags')).filter(c__gte=1)
    serializer_class = TagsByArticle;

class UpdateArticleView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ArticleSerializer
    queryset= Article.objects.all()

class NewArticleView(generics.CreateAPIView):
    serializer_class = ArticleSerializer
    queryset= Article.objects.all()

class NewTagView(generics.CreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagChangeSerializer

class FormMetaView(MultipleModelAPIView):
    queryList = [
        (Company.objects.all().order_by('name'),CompanySerializer),
        (EthicsSubCategory.objects.select_related('category').prefetch_related('tag_types').all(),EthicsSubSerializer)
    ]

class UpdateTagView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TagChangeSerializer
    queryset = Tag.objects.all()

class NewTagTypeView(generics.CreateAPIView):
    queryset = TagType.objects.all()
    serializer_class = TagTypeUpdateSerializer