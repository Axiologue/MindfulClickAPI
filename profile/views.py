from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from profile.models import TagPref
from profile.populate import populate_neutral
from profile.serializers import TagPrefSerializer
from profile.scoring import get_company_score
from tags.models import EthicsType, EthicsCategory
from refData.models import Company

class EthicsProfileView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        user = self.request.user
       
        # Fill in any new Tags as neutral
        if EthicsType.objects.count() > user.preferences.all().count():
            populate_neutral(user)

        # Get the user's current profiles
        prefs = user.preferences.select_related('tag_type').all()

        ethics = EthicsCategory.objects.all().prefetch_related('subcategories')

        data = [
            {'category':cat.name,
             'sub':[
                 {'sub': sub.name, 
                  'prefs': [
                      {'type':pref.tag_type.name,
                       'id':pref.id,
                       'preference':pref.preference
                       } for pref in prefs if pref.tag_type.subcategory_id == sub.id]
                  } for sub in cat.subcategories.all()]
             } for cat in ethics]

        return Response(data) 

class PrefUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TagPrefSerializer
    permission_classes = (IsAuthenticated,)
    queryset = TagPref.objects.all()

class CompanyScoreView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request,*args,**kwargs):
        user = self.request.user
        company = Company.objects.get(id=self.kwargs['pk'])

        return Response(get_company_score(company,user))
