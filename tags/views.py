from tags.models import Company 
from tags.models import EthicsTag, MetaTag, EthicsType, EthicsSubCategory
from refData.serializers import CompanySerializer
from tags.serializers import  EthicsTagChangeSerializer, \
        EthicsTypeSerializer, EthicsSubSerializer, EthicsTypeUpdateSerializer

from drf_multiple_model.views import MultipleModelAPIView

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

class NewEthicsTagView(generics.CreateAPIView):
    queryset = EthicsTag.objects.all()
    serializer_class = EthicsTagChangeSerializer
    permission_classes = (IsAuthenticated,)    
    
    def create(self, request, *args, **kwargs):
        request.data['added_by'] = request.user.id
        return super(NewArticleView,self).create(request,*args,**kwargs)

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
