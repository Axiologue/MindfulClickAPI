from rest_framework.test import APITestCase, APIRequestFactory, APIClient, force_authenticate
from rest_framework import status
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.test import TestCase

from profile.views import EthicsProfileView, PrefUpdateView, CompanyScoreView, QuestionAnswersView, \
        UpdateAnswersView, NewAnswerView, UserAnsweredView, SetAnswersView, ProductFetchView, \
        ProductFetchOverallOnlyView
from profile.populate import populate_preferences, populate_modifiers, populate_with_answers
from profile.models import Preference, Modifier, Answer, Question, ProfileMeta
from profile.scoring import get_company_score, get_product_score, get_combined_score
from tags.models import EthicsType, EthicsTag
from references.models import Company, Product

import os
import json

factory = APIRequestFactory()

class ProfileLogicTests(TestCase):
    
    fixtures = ['AuthTest','ArticleTestInput','TestCategories','TestCompanies','TestTags']

    maxDiff = None

    def setUp(self):
        self.user = User.objects.get(id=1)

        path = os.environ['DJANGO_PATH']

        # JSON file that holds the expect output of the tests
        # Also used in front end tests
        with open(path + '/references/fixtures/ArticleTestOutput.json') as data:
            self.output = json.load(data)

        # JSON file that holds post/put data for tests
        with open(path + '/references/fixtures/ArticlePostData.json') as postData:
            self.postData = json.load(postData)

    def test_populate_preferences_empty(self):
        # Confirm that are no current Ethical Preferences
        self.assertEqual(Preference.objects.count(),0)
        self.assertEqual(self.user.preferences.count(),0)

        # run the populate preferences function
        populate_preferences(self.user)

        # Check the new Preference counts
        self.assertEqual(Preference.objects.count(),5)
        self.assertEqual(self.user.preferences.count(),5)

        # Make sure all pref values are set to 0
        for pref in Preference.objects.all():
            self.assertEqual(pref.preference,0)

    def test_populate_preferences_not_empty(self):
        # Create a few manual preferences
        tt = EthicsType.objects.get(id=1) 
        Preference(user=self.user,tag_type=tt,preference=-4).save()

        tt = EthicsType.objects.get(id=2) 
        Preference(user=self.user,tag_type=tt,preference=3).save()

        tt = EthicsType.objects.get(id=3) 
        Preference(user=self.user,tag_type=tt,preference=-2).save()

        # Confirm that are the right number of Ethical Preferences
        self.assertEqual(Preference.objects.count(),3)
        self.assertEqual(self.user.preferences.count(),3)

        # run the populate preferences function
        populate_preferences(self.user)

        # Check the new Preference counts
        self.assertEqual(Preference.objects.count(),5)
        self.assertEqual(self.user.preferences.count(),5)

        # Check that the right number of Preferences are 0
        self.assertEqual(Preference.objects.filter(preference=0).count(),2)

    def test_get_company_score(self):
        # Create some preferences
        tt = EthicsType.objects.get(id=1) 
        Preference(user=self.user,tag_type=tt,preference=-4).save()

        tt = EthicsType.objects.get(id=2) 
        Preference(user=self.user,tag_type=tt,preference=3).save()

        tt = EthicsType.objects.get(id=4) 
        Preference(user=self.user,tag_type=tt,preference=-2).save()

        # Confirm that are the right number of Ethical Preferences
        self.assertEqual(Preference.objects.count(),3)
        self.assertEqual(self.user.preferences.count(),3)

        company = Company.objects.get(id=1)
        user = self.user

        results = get_company_score(company,user)

        # Confirm that new, preferences prefernces were created
        self.assertEqual(Preference.objects.count(),5)
        self.assertEqual(self.user.preferences.count(),5)

        self.assertEqual(results,self.output[23])

    def test_get_company_score_averages(self):
        # Create some preferences
        type1 = EthicsType.objects.get(id=1) 
        Preference(user=self.user,tag_type=type1,preference=-4).save()

        type2 = EthicsType.objects.get(id=2) 
        Preference(user=self.user,tag_type=type2,preference=3).save()

        type3 = EthicsType.objects.get(id=5)
        Preference(user=self.user,tag_type=type3,preference=-1).save()

        # Create some tags that share categories
        company = Company.objects.get(id=1)
        user = self.user

        EthicsTag(company=company,
                added_by=user,
                excerpt="Company used slaves",
                tag_type=type1,
                article_id=1).save()

        EthicsTag(company=company,
                added_by=user,
                excerpt="Just Kidding.  Company didn't actually use slaves",
                tag_type=type2,
                article_id=1).save()
        
        EthicsTag(company=company,
                added_by=user,
                excerpt="lots of accidents",
                tag_type=type3,
                article_id=1).save()
        
        results = get_company_score(company,user)
        self.assertEqual(results['categories'][0]['count'],1) # Number of Environment tags
        self.assertEqual(results['categories'][1]['count'],3) # Number of Labor tags
        self.assertEqual(results['categories'][1]['subcategories'][0]['score'],-1) # Slave Labor
        self.assertEqual(results['categories'][1]['subcategories'][1]['score'],-1) # Worker Safety
        self.assertEqual(results['categories'][1]['score'],-1) # Overall Labor score, rounded to the nearest 10th
        self.assertEqual(results['overall'],-1)

    def test_product_scores(self):
        # Create preferences and tags for both product and companies
        type1 = EthicsType.objects.get(id=1) 
        Preference(user=self.user,tag_type=type1,preference=-4).save()

        type2 = EthicsType.objects.get(id=2) 
        Preference(user=self.user,tag_type=type2,preference=3).save()

        type3 = EthicsType.objects.get(id=4)
        Preference(user=self.user,tag_type=type3,preference=-1).save()

        # Create some tags that share categories
        company = Company.objects.get(id=1) # Nike
        product = Product.objects.get(id=1) # Nike Flex Run
        user = self.user

        EthicsTag(company=company,
                added_by=user,
                excerpt="Company used slaves",
                tag_type=type1,
                article_id=1).save()

        EthicsTag(company=company,
                product=product,
                added_by=user,
                excerpt="Just kidding.  Company didn't actually use slaves",
                tag_type=type2,
                article_id=1).save()
        
        EthicsTag(company=company,
                added_by=user,
                excerpt="Too much carbon produced",
                tag_type=type3,
                article_id=1).save()

        product_score = get_product_score(product, self.user)
        company_score = get_company_score(company, self.user)
        combined_score = get_combined_score(product, self.user)

        self.assertEqual(product_score['categories'][0]['score'],0) # individual product Environment score
        self.assertEqual(product_score['categories'][1]['score'],3) # individual product Labor score
        self.assertEqual(company_score['categories'][0]['score'],-1) # overall company Environment score (excluding product)
        self.assertEqual(company_score['categories'][1]['score'],-4) # overall company Labor score (excluding product)
        self.assertEqual(combined_score['categories'][0]['score'],-1) # combined Environment score 
        self.assertEqual(combined_score['categories'][1]['score'],-1) # combined  company Labor score 

    def test_populate_modifiers_empty(self):
        # Check that there are no modifiers
        self.assertEqual(Modifier.objects.count(),0)
        answer = Answer.objects.get(id=1)
        self.assertEqual(answer.modifiers.count(),0)
        
        populate_modifiers(answer)

        # Check that we have the new right amount of Modifiers
        self.assertEqual(Modifier.objects.count(),5)
        self.assertEqual(answer.modifiers.count(),5)

        # Check that the scores on that given answer are all 0
        for mod in answer.modifiers.all():
            self.assertEqual(mod.modifier,0)

    def test_populate_modifiers_not_empty(self):
        answer = Answer.objects.get(id=1)

        # Create a few manual preferences
        tt = EthicsType.objects.get(id=1) 
        Modifier(answer=answer,tag_type=tt,modifier=-2).save()

        tt = EthicsType.objects.get(id=2) 
        Modifier(answer=answer,tag_type=tt,modifier=2).save()

        tt = EthicsType.objects.get(id=3) 
        Modifier(answer=answer,tag_type=tt,modifier=-1).save()

        # Check that there are no modifiers
        self.assertEqual(Modifier.objects.count(),3)
        answer = Answer.objects.get(id=1)
        self.assertEqual(answer.modifiers.count(),3)
        
        populate_modifiers(answer)

        # Check that we have the new right amount of Modifiers
        self.assertEqual(Modifier.objects.count(),5)
        self.assertEqual(answer.modifiers.count(),5)

        # Check that the new scores on the answer are 0
        self.assertEqual(answer.modifiers.filter(modifier=0).count(),2)

    def test_populate_with_answers(self):
        answer = Answer.objects.get(id=1)

        # Create a few manual preferences
        tt = EthicsType.objects.get(id=1) 
        Modifier(answer=answer,tag_type=tt,modifier=-2).save()

        tt = EthicsType.objects.get(id=2) 
        Modifier(answer=answer,tag_type=tt,modifier=2).save()

        tt = EthicsType.objects.get(id=3) 
        Modifier(answer=answer,tag_type=tt,modifier=-1).save()

        self.assertEqual(self.user.preferences.count(),0)

        populate_with_answers(self.user)

        # Make sure nothing happens until we apply the answers to the user
        self.assertEqual(self.user.preferences.filter(preference=0).count(),5)

        # Apply the answer to the user, and then run populate with answers again
        answer.users.add(self.user)
        populate_with_answers(self.user)
       
        # Check that our scores are appropriately modified
        pref = Preference.objects.get(user=self.user,tag_type_id=1)
        self.assertEqual(pref.preference,-2)

        # Check that our scores are appropriately modified
        pref = Preference.objects.get(user=self.user,tag_type_id=2)
        self.assertEqual(pref.preference,2)

        # Check that our scores are appropriately modified
        pref = Preference.objects.get(user=self.user,tag_type_id=3)
        self.assertEqual(pref.preference,-1)

        # Check that our scores are appropriately modified
        pref = Preference.objects.get(user=self.user,tag_type_id=4)
        self.assertEqual(pref.preference,0)

        # Check that our scores are appropriately modified
        pref = Preference.objects.get(user=self.user,tag_type_id=4)
        self.assertEqual(pref.preference,0)

        # Ensure modifiers aren't rerun when populating again
        populate_with_answers(self.user)

        # Check that our scores are appropriately modified
        pref = Preference.objects.get(user=self.user,tag_type_id=1)
        self.assertEqual(pref.preference,-2)


class ProfileViewTests(APITestCase):

    fixtures = ['AuthTest','ArticleTestInput','TestCategories','TestCompanies','TestTags']

    maxDiff = None

    def setUp(self):
        path = os.environ['DJANGO_PATH']

        # get user for views
        self.user = User.objects.get(id=1)

        # instantiate client for testing actual URLS
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # JSON file that holds the expect output of the tests
        # Also used in front end tests
        with open(path + '/references/fixtures/ArticleTestOutput.json') as data:
            self.output = json.load(data)

        # JSON file that holds post/put data for tests
        with open(path + '/references/fixtures/ArticlePostData.json') as postData:
            self.postData = json.load(postData)

    # Test EthicsProfileView with no set Preferences
    def test_ethics_profile_view(self):
        # Count initial count of Preference objects
        self.assertEqual(Preference.objects.count(),0)
        self.assertEqual(self.user.preferences.count(),0)

        view = EthicsProfileView.as_view()

        request = factory.get('profile/prefs/all/')
        force_authenticate(request, user=self.user)
        response = view(request).render()

        self.assertEqual(response.status_code,status.HTTP_200_OK)

        # Count the appropriate amount of Preferences objects were made
        self.assertEqual(Preference.objects.count(),5)
        self.assertEqual(self.user.preferences.count(),5)
        
        # Check the output
        self.assertEqual(response.data,self.output[21])

    # Test for EthicsProfileView url endpoints
    def test_ethics_profile_view_url(self):
        response = self.client.get('/profile/prefs/all/')

        self.assertEqual(response.status_code,status.HTTP_200_OK)

    # Test for PrefUpdateView
    # Alters a single Pref
    def test_pref_update_view(self):
        # Create single Preference object to alter
        et = EthicsType.objects.get(id=1)
        t = Preference(user=self.user,tag_type=et,preference=2)
        t.save()

        view = PrefUpdateView.as_view()

        request = factory.put('profile/prefs/{0}/'.format(t.id),self.postData[13])
        force_authenticate(request,user=self.user)
        response = view(request,pk=t.id).render()

        self.assertEqual(response.status_code,status.HTTP_200_OK)

        # Check that the updated Preference object's preference is now set to 5
        t = Preference.objects.get(id=t.id)
        self.assertEqual(t.preference,5)

    # Test for CompanyScoreView
    def test_get_company_score_view(self):
        # Create some preferences
        tt = EthicsType.objects.get(id=1) 
        Preference(user=self.user,tag_type=tt,preference=-4).save()

        tt = EthicsType.objects.get(id=2) 
        Preference(user=self.user,tag_type=tt,preference=3).save()

        tt = EthicsType.objects.get(id=4) 
        Preference(user=self.user,tag_type=tt,preference=-2).save()
        
        view = CompanyScoreView.as_view()

        request = factory.get('/profile/scores/company/1/')
        force_authenticate(request,user=self.user)
        response = view(request,pk=1).render()

        self.assertEqual(response.status_code,status.HTTP_200_OK)

        # Compare the ouptput the expected 
        self.assertEqual(response.data, self.output[23])

    def test_get_company_score_view_url(self):
        tt = EthicsType.objects.get(id=4) 
        Preference(user=self.user,tag_type=tt,preference=-2).save()

        response = self.client.get('/profile/scores/company/1/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Compare the ouptput the expected 
        self.assertEqual(response.data, self.output[23])

    # Test for QuestionAnswersView
    def test_question_answers_view(self):
        view = QuestionAnswersView.as_view()
        
        request = factory.get('/profile/question/answers/1/')
        force_authenticate(request,user=self.user)
        response = view(request,pk=1).render()

        self.assertEqual(response.status_code,status.HTTP_200_OK)

        # Compare the output with the expected json
        test_data = self.output[25];
        test_data['question']['supplement'] = None
        for answer in test_data['answers']:
            answer['modifiers'] = {1:0,2:0,3:0,4:0,5:0}
        self.assertEqual(response.data, test_data)

    def test_question_answers_view_url(self):
        response = self.client.get('/profile/question/answers/1/')

        self.assertEqual(response.status_code,status.HTTP_200_OK)

        # Compare the output with the expected json
        test_data = self.output[25];
        test_data['question']['supplement'] = None
        for answer in test_data['answers']:
            answer['modifiers'] = {1:0,2:0,3:0,4:0,5:0}
        self.assertEqual(response.data, test_data)

    # Test for UpdateAnswersView
    def test_update_answers_view(self):
        data = self.postData[15]

        # Get Blank modifiers
        for ans in data:
            answer = Answer.objects.get(id=ans['id'])
            populate_modifiers(answer)

        self.assertEqual(15,Modifier.objects.filter(modifier=0).count())

        view = UpdateAnswersView.as_view()

        request = factory.put('/profile/question/answer/1/updateAll/',self.postData[15],format="json")
        force_authenticate(request,user=self.user)
        response = view(request,pk=1).render()

        self.assertEqual(response.status_code,status.HTTP_200_OK)

        # Check that the modifier scores are now adjusted
        self.assertEqual(5,Modifier.objects.filter(modifier=-1).count())
        self.assertEqual(3,Modifier.objects.filter(modifier=-2).count())
        self.assertEqual(4,Modifier.objects.filter(modifier=0).count())

    # Test NewAnswerView
    def test_new_answer_view(self):
        # Check initial states
        self.assertEqual(Answer.objects.count(), 3)
        
        question = Question.objects.get(id=1)
        self.assertEqual(question.answers.count(),3)

        for answer in Answer.objects.all():
            populate_modifiers(answer)

        self.assertEqual(Modifier.objects.count(),15)

        view = NewAnswerView.as_view()

        request = factory.post('/profile/question/answer/1/new/',self.postData[17])
        force_authenticate(request,user=self.user)
        response = view(request,pk=1).render()

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

        self.assertEqual(Answer.objects.count(),4)
        self.assertEqual(question.answers.count(),4)
        self.assertEqual(Modifier.objects.count(),20)

    # Test UserAnsweredView
    def test_user_answered_view(self):
        view = UserAnsweredView.as_view()

        # Test Default Setting
        request = factory.get('/profile/meta/answered/')
        force_authenticate(request,user=self.user)
        response = view(request)

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data,{'answered':False})

        ProfileMeta(user=self.user,answered=True).save()

        # Test after answered questions
        request = factory.get('/profile/meta/answered/')
        force_authenticate(request,user=self.user)
        response = view(request)

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data,{'answered':True})

    # Test SetAnswersView
    def test_set_answers_view(self):
        # test defaults
        self.assertEqual(0,self.user.answered.count())
        with self.assertRaises(ObjectDoesNotExist):
            self.user.meta.answered

        # Set up some default modifier values
        answer = Answer.objects.get(id=2)
        modifiers = {
            1: -1,
            2: 1,
            3: -2,
            4: 0,
            5: -1
        }
        populate_modifiers(answer)
        for i in range(1,6):
            modifier = Modifier.objects.get(answer=answer,tag_type_id=i)
            modifier.modifier = modifiers[i]
            modifier.save()

        view = SetAnswersView.as_view()

        request = factory.post('/profile/question/answers/set',self.postData[19])
        force_authenticate(request, user=self.user)
        response = view(request)

        self.assertEqual(response.status_code,status.HTTP_200_OK)

        self.assertEqual(1,self.user.answered.count())
        self.assertEqual(self.user.preferences.get(tag_type_id=1).preference,-1)
        self.assertEqual(self.user.preferences.get(tag_type_id=2).preference,1)
        self.assertEqual(self.user.preferences.get(tag_type_id=3).preference,-2)
        self.assertEqual(self.user.preferences.get(tag_type_id=4).preference,0)
        self.assertEqual(self.user.preferences.get(tag_type_id=5).preference,-1)

    # Test ProductFetchView
    def test_product_fetch_view(self):
        view = ProductFetchView.as_view()

        # Create base preferences
        self.user.preferences.create(tag_type_id=4,preference=-2)

        request = factory.post('/articles/products/fetch/',{"product":'flex run',"brand":"Nike"})
        force_authenticate(request, user=self.user)
        response = view(request).render()

        self.assertEqual(response.status_code,status.HTTP_200_OK)

        data = {
                'product': self.output[31],
                'company': self.output[23]
                }

        self.assertEqual(response.data,data)

    # Test ProductFetchView with product not in database
    def test_product_fetch_view_no_match(self):
        view = ProductFetchView.as_view()

        request = factory.post('/articles/products/fetch/',{"product":'badonkadonk',"brand":"Blizzles"})
        force_authenticate(request, user=self.user)
        response = view(request).render()

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data,{'error': 'No product match'})

    def test_product_fetch_overall_only_view(self):
        view = ProductFetchOverallOnlyView.as_view()

        # Create base preferences
        self.user.preferences.create(tag_type_id=4,preference=-2)

        request = factory.post('/articles/products/fetch/',{"product":'flex run',"brand":"Nike"})
        force_authenticate(request, user=self.user)
        response = view(request).render()

        self.assertEqual(response.status_code,status.HTTP_200_OK)

        data = {
                'product': self.output[31],
                'score': -2.0 
                }

        self.assertEqual(response.data,data)
