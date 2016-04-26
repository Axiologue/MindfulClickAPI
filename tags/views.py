from .models import EthicsTag, MetaTag, EthicsType, EthicsSubCategory, EthicsCategory
from .serializers import  EthicsTagChangeSerializer, MetaTagSerializer, \
        EthicsTypeSerializer, EthicsSubSerializer, EthicsTypeUpdateSerializer, \
        EthicsTagByObjectSerializer
from products.models import Company
from products.serializers import CompanySerializer

from drf_multiple_model.views import MultipleModelAPIView

from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import django_filters

class NewEthicsTagView(generics.CreateAPIView):
    queryset = EthicsTag.objects.all()
    serializer_class = EthicsTagChangeSerializer
    permission_classes = (IsAuthenticated,)    
    
    def create(self, request, *args, **kwargs):
        request.data['added_by'] = request.user.id

        # create Tag data for each product, if given
        if request.data.get('products',None):
            data = []
            for product in request.data['products']:
                tagData = request.data.copy()
                tagData['product'] = product['id']
                tagData.pop('products',None)
                data.append(tagData)
            serializer = self.serializer_class(data=data,many=True)
        else:
            request.data.pop('products', None)
            serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class FormMetaView(MultipleModelAPIView):
    queryList = [
        (Company.objects.all().order_by('name'),CompanySerializer),
        (EthicsSubCategory.objects.select_related('category').prefetch_related('tag_types').all(),EthicsSubSerializer)
    ]

class UpdateEthicsTagView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EthicsTagChangeSerializer
    queryset = EthicsTag.objects.all()
    permission_classes = (IsAuthenticated,)    

class NewEthicsTypeView(generics.CreateAPIView):
    queryset = EthicsType.objects.all()
    serializer_class = EthicsTypeUpdateSerializer
    permission_classes = (IsAuthenticated,)    

class NoRelDataView(generics.CreateAPIView):
    queryset = MetaTag.objects.all()
    serializer_class = MetaTagSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        request.data['added_by'] = request.user.id
        return super(NoRelDataView,self).create(request,*args,**kwargs)

class UpdateMetaTagView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MetaTag.objects.all()
    serializer_class = MetaTagSerializer


class EthicsTagFilter(django_filters.FilterSet):
    company = django_filters.CharFilter(name='company__name', lookup_type='icontains')
    product = django_filters.CharFilter(name='product__name', lookup_type='icontains')
    company_id = django_filters.NumberFilter(name='company_id')
    product_id = django_filters.NumberFilter(name='product_id')
    no_product = django_filters.BooleanFilter(name='product', lookup_type='isnull')
    
    class Meta:
        model = EthicsTag


class TagsByObjectView(generics.ListAPIView):
    serializer_class = EthicsTagByObjectSerializer
    queryset = EthicsTag.objects.select_related(
            'tag_type', 
            'tag_type__subcategory__category',
            'reference',
            'added_by')
    filter_class = EthicsTagFilter
    filter_backends = (filters.DjangoFilterBackend,)

    # split tag types into categories before returning
    def list(self, request, *arg, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        tag_data = serializer.data

        categories = EthicsCategory.objects.all()
        data = [{'category': x.name, 'tags': [y for y in tag_data if y['category'] == x.name]} for x in categories]

        return Response(data)
