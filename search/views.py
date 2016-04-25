from rest_framework.views import APIView
from rest_framework.response import Response
from haystack.query import RelatedSearchQuerySet 

from products.serializers import ProductSimpleSerializer, CompanySimpleSerializer
from products.models import Product, Company
from references.serializers import ReferenceSerializer
from references.models import Reference

class GeneralSearchView(APIView):
    def get(self, request, *args, **kwargs):
        search_term = request.query_params.get('q', None)

        if search_term is None:
            return Response({'error': 'You must provide a \'q\' search paramater with your request'})

        query = self.get_query(search_term)

        data = self.serialize_query(query)

        return Response(data)
    
    def get_query(self, search_term):
        return RelatedSearchQuerySet().filter(content=search_term)

    def serialize_query(self, queryset):

        products = [{'text': x.get_stored_fields()['text'], 'id': x.pk} for x in queryset if x.model == Product] 
        companies = [{'text': x.get_stored_fields()['text'], 'id': x.pk} for x in queryset if x.model == Company] 
        references = [{'text': x.get_stored_fields()['text'], 'id': x.pk} for x in queryset if x.model == Reference] 

        data = {
            'products': products,
            'companies': companies,
            'references': references,
        }

        return data
