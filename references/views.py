from .models import Article, Product, Company
from .serializers import ArticleSerializer, ProductSerializer, ProductSimpleSerializer, \
       ArticleEthicsTagsSerializer, ArticleMetaTagsSerializer, CompanySerializer, NewProductSerializer
from tags.models import EthicsType, EthicsTag
from profile.scoring import get_company_score, get_combined_score

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.response import Response
from django.db.models import Count, Prefetch
import django_filters

class ArticleNoTagView(generics.ListAPIView):
    queryset = Article.objects.annotate(c=Count('ethicstags',distinct=True),
            d=Count('metatags')).filter(c=0,d=0)
    serializer_class = ArticleSerializer


class ArticleWithCrossView(generics.ListAPIView):
    queryset= Article.objects.prefetch_related(
        'ethicstags__company',
        Prefetch('ethicstags__tag_type', queryset=EthicsType.objects.select_related('subcategory'))
        ).annotate(c=Count('ethicstags')).filter(c__gte=1)
    serializer_class = ArticleEthicsTagsSerializer;


class ArticleWithCrossByCompanyView(generics.ListAPIView):
    serializer_class = ArticleEthicsTagsSerializer;

    def get_queryset(self):
        return Article.objects.prefetch_related(
            Prefetch('ethicstags', queryset=EthicsTag.objects.select_related('company').filter(company_id=self.kwargs['pk'])),
            Prefetch('ethicstags__tag_type', queryset=EthicsType.objects.select_related('subcategory')),
            ).annotate(c=Count('ethicstags')).filter(c__gte=1,ethicstags__company_id=self.kwargs['pk'])


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


class ArticleNoDataView(generics.ListAPIView):
    serializer_class = ArticleMetaTagsSerializer
    queryset = Article.objects.filter(metatags__tag_type=1)


class AllCompaniesView(generics.ListAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()


class SingleCompanyView(generics.RetrieveAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()


class ProductListFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_type='icontains')
    company = django_filters.CharFilter()
    price = django_filters.RangeFilter()

    class Meta:
        model = Product
        fields = ['name','company_id','category','division','price']


class ProductListView(generics.ListAPIView):
    model = Product
    serializer_class = ProductSimpleSerializer
    queryset = Product.objects.select_related('company').all()

    # Filter tools
    filter_class = ProductListFilter
    filter_backends = (filters.DjangoFilterBackend,)

    # Reformat response to best process fir angucomplete format
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        data = {'products': serializer.data}

        return Response(data)


# New Product Endpoint
class ProductNewView(generics.CreateAPIView):
    serializer_class = NewProductSerializer
    queryset = Product.objects.all()


class SingleProductView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

