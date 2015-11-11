from tags.models import Company 
from tags.models import EthicsTag, MetaTag, EthicsType, EthicsSubCategory
from refData.serializers import CompanySerializer
from tags.serializers import  EthicsTagChangeSerializer, MetaTagSerializer, \
        EthicsTypeSerializer, EthicsSubSerializer, EthicsTypeUpdateSerializer

from drf_multiple_model.views import MultipleModelAPIView

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class NewEthicsTagView(generics.CreateAPIView):
    queryset = EthicsTag.objects.all()
    serializer_class = EthicsTagChangeSerializer
    permission_classes = (IsAuthenticated,)    
    
    def create(self, request, *args, **kwargs):
        request.data['added_by'] = request.user.id

        # create Tag data for each product, if given
        if request.data['products']:
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
