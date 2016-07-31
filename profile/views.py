import itertools
from json import JSONDecoder
import json

from rest_framework import generics, status, exceptions, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

from .models import Preference, Question, Answer, Modifier
from .populate import populate_preferences, populate_modifiers, populate_with_answers
from .serializers import PreferenceSerializer, QuestionSerializer, AnswerSerializer, \
        QuestionAnswerSerializer
from .scoring import get_company_score, get_combined_score
from tags.models import EthicsType, EthicsCategory
from products.models import Company, Product
from products.fetch import fuzzy_fetch 
from products.serializers import ProductSerializer, CompanySerializer



# List all the Ethical Preferences of a User
class EthicsProfileView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)

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
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Preference.objects.all()


# List All Current Questions for Profile Setting
class QuestionListView(generics.ListAPIView):
    permission_classes = (permissions.IsAdminUser, )
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


# Same as Above, but includes answers
class QuestionWithAnswersListView(QuestionListView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = QuestionAnswerSerializer


# For new Profile setting questions
class NewQuestionView(generics.CreateAPIView):
    permission_classes = (permissions.IsAdminUser, )
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


# Gives Given modifiers for all answers in a given question
# Used to view and alter the modifiers for ALL answers to a given question
class QuestionAnswersView(generics.ListAPIView):
    permission_classes = (permissions.IsAdminUser, )
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
    permission_classes = (permissions.IsAdminUser, )
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
    permission_classes = (permissions.IsAdminUser, )
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
    permission_classes= (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = self.request.user

        try:
            answered = user.initial_answers
        except ObjectDoesNotExist:
            answered = False

        return Response({"answered": answered})


# View that takes the chosen answers for a users and applies them to a base profile
class SetAnswersView(APIView):
    permission_classes= (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user

        # Get an array of answer IDs, and set the user as having chosen that answer
        answers = Answer.objects.filter(id__in=request.data['answers'])

        for answer in answers:
            answer.users.add(user)

        # Apply answer modifiers for that user
        populate_with_answers(user)

        user.initial_answers = True
        user.save()

        return Response(status=status.HTTP_200_OK)



# Get scores of Generic users by company
# Also returns user score if user is logged in
class BaseGenericScoreView(generics.RetrieveAPIView):
    serializer_class = None
    queryset = None
    score_function = None

    # view settings flags
    include_object = True
    include_subcategories = True
    use_fuzzy_fetch = True
    use_generics = True


    def retrieve(self, request, *args, **kwargs):
        users = self.get_users()

        # Try to get the object and catch various exceptions
        try:
            obj = self.get_object()
        except ObjectDoesNotExist as e:
            return Response({'error': str(e)})
        except KeyError as e:
            return Response({'error': str(e)})

        scores = self.get_scores(obj, users)

        include_object = self.get_boolean_from_request(request, 'include_object')

        if include_object:
            serializer = self.get_serializer(obj)

            data = {
                self.queryset.model.__name__: serializer.data,
                'scores': scores
            }

        else:
            data = scores

        return Response(data)

    def get_scores(self, obj, users):
        """
        returns list of users and their scores
        """

        return [
            dict(itertools.chain({'user': user.username}.items(), self.get_individual_score(obj, user).items())) 
            for user in users
        ]

    def get_individual_score(self, obj, user):
        """
        Gets a score for a product or company
        Returns only the overall score if `include_subcategories` is set to false
        """

        score_func = self.get_score_function()

        include_subcategories = self.get_boolean_from_request(self.request, 'include_subcategories')

        return score_func(obj, user) if include_subcategories else {'overall': score_func(obj, user)['overall']}
    
    def get_score_function(self):
        """
        Return the scoring function for this object/set
        Defaults to using `self.score_function`.
        """
        
        assert self.score_function is not None, (
            "'%s' should either include a `score_function` attribute, "
            "or override the `get_score_function` method."
            % self.__class__.__name__
        )

        return self.score_function

    def get_users(self):
        """
        By default, returns a list with Generic users and the current user (if authenticated)
        """
        use_generics = self.get_boolean_from_request(self.request, 'use_generics')

        users = []

        if self.request.user.is_authenticated():
           users.append(self.request.user)

        if use_generics:
            User = get_user_model() 
            users += list(User.objects.filter(generic=True))

        if not users:
            raise exceptions.AuthenticationFailed('Please Log in to See Your Scores')

        return users
       
    def get_object(self):
        """
        Returns object based on query params
        requires either 'id' or 'name' in the query_params
        """

        if 'id' not in self.request.query_params and 'name' not in self.request.query_params:
            raise KeyError('This view requires a querystring with a name or id attribute')

        queryset = self.get_queryset()

        if 'name' in self.request.query_params:
            if self.use_fuzzy_fetch:
                try:
                    obj = fuzzy_fetch(queryset, self.request.query_params['name'])
                except ObjectDoesNotExist as e:
                    raise ObjectDoesNotExist(str(e)) 

            else:
                obj = queryset.get(name=self.request.query_params['name'])

        else:
            obj = queryset.get(id=self.request.query_params['id'])

        return obj

    def get_boolean_from_request(self, request, key):
        """
        Checks for a certain boolean querystring.
        If present, returns appropriate true/false value
        else, returns default class setting for value
        """

        if key in request.query_params:
            val = request.query_params[key]

            if val == 'True' or val == 'true':
                return True

            else:
                return False

        else:
            return getattr(self, key)


# Get the personalized score of a given user
class CompanyScoreView(BaseGenericScoreView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    score_function = staticmethod(get_company_score)
    use_fuzzy_fetch = False


# View for getting ALL current company scores
class CompanyScoreAllView(CompanyScoreView):

    def get(self, request, *args, **kwargs):
        return self.list(request, args, kwargs)

    def list(self, request, *args, **kwargs):
        users = self.get_users()

        all_scores = []
        for obj in self.queryset.all():
            scores = self.get_scores(obj, users)

            serializer = self.get_serializer(obj)

            data = {
                self.queryset.model.__name__: serializer.data,
                'scores': scores
            }

            all_scores.append(data)

        return Response(all_scores)
    


# Get the personalized score for a user/product pair
class ProductScoreView(BaseGenericScoreView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    score_function = staticmethod(get_combined_score)


