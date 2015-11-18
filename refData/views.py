from refData.models import Article, Product, Company
from tags.models import EthicsType
from refData.serializers import ArticleSerializer, ProductSerializer, ProductSimpleSerializer, \
       ArticleEthicsTagsSerializer, ArticleMetaTagsSerializer, CompanySerializer
from profile.scoring import get_company_score

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.response import Response
from django.db.models import Count, Prefetch
import django_filters

from fuzzywuzzy import fuzz, process

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

class ProductListFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_type='icontains')
    company = django_filters.CharFilter()

    class Meta:
        model = Product
        fields = ['name','company_id']

class ProductListView(generics.ListAPIView):
    model = Product
    serializer_class = ProductSimpleSerializer
    queryset = Product.objects.all()

    # Filter tools
    filter_class = ProductListFilter
    filter_backends = (filters.DjangoFilterBackend,)

    # Reformat response to best process fir angucomplete format
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        data = {'products': serializer.data}

        return Response(data)

# Use fuzzy matching to find best product match
class ProductFetchView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer

        products = Product.objects.all()
        names_list = [x.name for x in products]
        product_string = process.extractOne(request.data['product'],names_list,scorer=fuzz.token_set_ratio)

        # Make sure there's a good enough match
        if product_string[1] > 80:
            product = Product.objects.filter(name=product_string[0])[0]

            user = request.user

            data = {
                    'product': serializer(product).data,
                    'company': get_company_score(product.company,user)
            }

            return Response(data)

        else:
            return Response({'error': 'No product match'})
