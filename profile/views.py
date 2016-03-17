from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

from .models import Preference, Question, Answer, Modifier, ProfileMeta
from .populate import populate_preferences, populate_modifiers, populate_with_answers
from .serializers import PreferenceSerializer, QuestionSerializer, AnswerSerializer, \
        QuestionAnswerSerializer
from .scoring import get_company_score, get_combined_score
from tags.models import EthicsType, EthicsCategory
from references.models import Company, Product
from references.fetch import product_fetch
from references.serializers import ProductSerializer

from json import JSONDecoder


# List all the Ethical Preferences of a User
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

# Alter a particular Preference
class PrefUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PreferenceSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Preference.objects.all()


# Get the personalized score of a given user
class CompanyScoreView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request,*args,**kwargs):
        user = self.request.user
        company = Company.objects.get(id=self.kwargs['pk'])

        return Response(get_company_score(company,user))


# Get the personalized score for a user/product pair
class ProductScoreView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        product = Product.objects.get(id=self.kwargs['pk'])

        return Response(get_combined_score(product,user))


class ProductScoreOverallOnlyView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        product = Product.objects.get(id=self.kwargs['pk'])

        return Response({'score': get_combined_score(product,user)['overall']})


# List All Current Questions for Profile Setting
class QuestionListView(generics.ListAPIView):
    #permission_classes = (IsAuthenticated,)
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


# Same as Above, but includes answers
class QuestionWithAnswersListView(QuestionListView):
    serializer_class = QuestionAnswerSerializer


# For new Profile setting questions
class NewQuestionView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


# Gives Given modifiers for all answers in a given question
# Used to view and alter the modifiers for ALL answers to a given question
class QuestionAnswersView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
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

        
# Update the modifiers for a given question
class UpdateAnswersView(generics.UpdateAPIView):
    def update(self,request, *args, **kwargs):
        data = request.data

        # Fetch the requested questions
        try:
            question = Question.objects.get(id=self.kwargs['pk'])
        except ObjectDoesNotExist:
            return Response({'error': 'No Question Matches that ID'})

        # iterate through answers, save any changes
        for answer in data:
            for modifier in Modifier.objects.filter(answer_id=answer['id']):
                score = answer['modifiers'].get(str(modifier.tag_type_id))
                if modifier.modifier != score and score:
                    modifier.modifier = score
                    modifier.save()

        return Response(data)


# Create a new answer
# Also needs to set a blank set of modifiers 
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


# View to check if the user has answered the profile setting questions
class UserAnsweredView(APIView):
    permission_classes= (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = self.request.user

        try:
            answered = user.meta.answered
        except ObjectDoesNotExist:
            answered = False

        return Response({"answered": answered})


# View that takes the chosen answers for a users and applies them to a base profile
class SetAnswersView(APIView):
    permission_classes= (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user

        # Get an array of answer IDs, and set the user as having chosen that answer
        answers = Answer.objects.filter(id__in=request.data['answers'])

        for answer in answers:
            answer.users.add(user)

        # Apply answer modifiers for that user
        populate_with_answers(user)

        try:
            user.meta.answered = True
            user.meta.save()
        except ObjectDoesNotExist:
            m = ProfileMeta(user=user,answered=True)
            m.save()

        return Response(status=status.HTTP_200_OK)


# Use fuzzy matching to find best product match
class ProductFetchView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer

        try:
            product = product_fetch(request.data['product'])

        except ObjectDoesNotExist:
            return Response({'error': 'No product match'})

        user = request.user
        data = {
                'product': serializer(product).data,
                'company': get_combined_score(product,user)
        }

        return Response(data)


# Use fuzzy matching to find best product match
# Returns only overall score
class ProductFetchOverallOnlyView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer

        try:
            product = product_fetch(request.data['product'])

        except ObjectDoesNotExist:
            return Response({'error': 'No product match'})

        user = request.user
        data = {
                'product': serializer(product).data,
                'score': get_combined_score(product,user)['overall']
        }

        return Response(data)
