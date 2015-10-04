from refData.models import Article, Product, EthicsSubCategory, Company, Tag, TagType
from refData.serializers import ArticleSerializer, ProductSerializer, \
        EthicsSubSerializer, CompanySerializer, TagsByArticle, TagChangeSerializer, TagSerializer, \
        TagTypeSerializer, TagTypeUpdateSerializer

from drf_multiple_model.views import MultipleModelAPIView

from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Prefetch

class ArticleNoTagView(generics.ListAPIView):
    queryset = Article.objects.annotate(c=Count('tags')).filter(c=0)
    serializer_class = ArticleSerializer

class ArticleWithCrossView(generics.ListAPIView):
    queryset= Article.objects.prefetch_related(
        'tags__company',
        Prefetch('tags__tag_type', queryset=TagType.objects.select_related('subcategory'))
        ).annotate(c=Count('tags')).filter(c__gte=1)
    serializer_class = TagsByArticle;

class UpdateArticleView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ArticleSerializer
    queryset= Article.objects.all()
    permission_classes = (IsAuthenticated,)    

class NewArticleView(generics.CreateAPIView):
    serializer_class = ArticleSerializer
    queryset= Article.objects.all()
    permission_classes = (IsAuthenticated,)    

    def create(self, request, *args, **kwargs):
        request.data['added_by'] = request.user.id
        return super(NewArticleView,self).create(request,*args,**kwargs)

class NewTagView(generics.CreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagChangeSerializer
    permission_classes = (IsAuthenticated,)    
    
    def create(self, request, *args, **kwargs):
        request.data['added_by'] = request.user.id
        return super(NewArticleView,self).create(request,*args,**kwargs)

class FormMetaView(MultipleModelAPIView):
    queryList = [
        (Company.objects.all().order_by('name'),CompanySerializer),
        (EthicsSubCategory.objects.select_related('category').prefetch_related('tag_types').all(),EthicsSubSerializer)
    ]

class UpdateTagView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TagChangeSerializer
    queryset = Tag.objects.all()
    permission_classes = (IsAuthenticated,)    

class NewTagTypeView(generics.CreateAPIView):
    queryset = TagType.objects.all()
    serializer_class = TagTypeUpdateSerializer
    permission_classes = (IsAuthenticated,)    
