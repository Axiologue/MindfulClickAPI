from .models import Product, Company
from .serializers import ProductSerializer, ProductSimpleSerializer, \
      CompanySerializer, NewProductSerializer
from profile.scoring import get_company_score, get_combined_score

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.response import Response
import django_filters


class AllCompaniesView(generics.ListAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()


class SingleCompanyView(generics.RetrieveAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()


class SingleByNameCompanyView(generics.RetrieveAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    lookup_field = 'name'


class ProductListFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_type='icontains')
    company = django_filters.CharFilter(name='company__name', lookup_type='icontains')
    price = django_filters.RangeFilter()

    class Meta:
        model = Product
        fields = ['name', 'company_id', 'price', 'category', 'company']


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSimpleSerializer
    queryset = Product.objects.select_related('company').all()

    # Filter tools
    filter_class = ProductListFilter
    filter_backends = (filters.DjangoFilterBackend,)

    # Reformat response to best process for angucomplete format
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

