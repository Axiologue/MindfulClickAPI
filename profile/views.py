from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

from profile.models import Preference, Question, Answer, Modifier
from profile.populate import populate_preferences, populate_modifiers
from profile.serializers import PreferenceSerializer, QuestionSerializer, AnswerSerializer
from profile.scoring import get_company_score
from tags.models import EthicsType, EthicsCategory
from refData.models import Company

class EthicsProfileView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        user = self.request.user
       
        # Fill in any new Tags as neutral
        if EthicsType.objects.count() > user.preferences.all().count():
            populate_preferences(user)

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
    serializer_class = PreferenceSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Preference.objects.all()

class CompanyScoreView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request,*args,**kwargs):
        user = self.request.user
        company = Company.objects.get(id=self.kwargs['pk'])

        return Response(get_company_score(company,user))

class QuestionListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class NewQuestionView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class QuestionAnswersView(generics.ListAPIView):
    #permission_classes = (IsAuthenticated,)
    queryset = EthicsCategory.objects.all()

    def list(self,requestion, *args, **kwargs):
        # Get list of Ethics Category for Answer table row
        categories = self.get_queryset()
        types = EthicsType.objects.select_related('subcategory').all()

        # Format Category and Types for use in tables
        ethicsData = []
        for category in categories:
            cat = {'name': category.name, 'tag_types': []}

            thisTypes = [t for t in types if t.subcategory.category_id == category.id]
            for t in thisTypes:
                tag_type = {'name': t.name, 'subcategory': t.subcategory.name, 'id':t.id}
                cat['tag_types'].append(tag_type)

            ethicsData.append(cat)
 
        # Fetch the requested questions
        try:
            question = Question.objects.get(id=self.kwargs['pk'])
        except ObjectDoesNotExit:
            return Response({'error': 'No Question Matches that ID'})
      
        # Manually serialize modifiers as dictionary for easy access in table
        answerData = []
        for answer in question.answers.all():
            ans = {'answer':answer.answer,'modifiers':{},'id':answer.id}
            populate_modifiers(answer)

            for modifier in answer.modifiers.all():
                ans['modifiers'][modifier.tag_type_id] = modifier.modifier

            answerData.append(ans)

        return Response({
            'ethics':ethicsData,
            'answers':answerData,
            'question': {
                    'question':question.question,
                    'supplement':question.supplement
                }
            })

class UpdateAnswersView(generics.UpdateAPIView):
    def update(self,request, *args, **kwargs):
        data = request.data

        # Fetch the requested questions
        try:
            question = Question.objects.get(id=self.kwargs['pk'])
        except ObjectDoesNotExit:
            return Response({'error': 'No Question Matches that ID'})

        # iterate through answers, save any changes
        for answer in data:
            for modifier in Modifier.objects.filter(answer_id=answer['id']):
                score = answer['modifiers'].get(str(modifier.tag_type_id))
                if modifier.modifier != score and score:
                    modifier.modifier = score
                    modifier.save()

        return Response(data)

class NewAnswerView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        answer = Answer.objects.get(question=serializer.data['question'],answer=serializer.data['answer']) 
        ans = {'answer':answer.answer,'modifiers':{},'id':answer.id}
        populate_modifiers(answer)

        for modifier in answer.modifiers.all():
            ans['modifiers'][modifier.tag_type_id] = modifier.modifier

        return Response(ans, status=status.HTTP_201_CREATED, headers=headers)


