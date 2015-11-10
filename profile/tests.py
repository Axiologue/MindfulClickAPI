from rest_framework.test import APITestCase, APIRequestFactory, APIClient, force_authenticate
from rest_framework import status
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.test import TestCase

from profile.views import EthicsProfileView, PrefUpdateView, CompanyScoreView
from profile.populate import populate_preferences, populate_modifiers, populate_with_answers
from profile.models import Preference, Modifier, Answer
from profile.scoring import get_company_score
from tags.models import EthicsType
from refData.models import Company

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
        with open(path + '/refData/fixtures/ArticleTestOutput.json') as data:
            self.output = json.load(data)

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
        with open(path + '/refData/fixtures/ArticleTestOutput.json') as data:
            self.output = json.load(data)

        # JSON file that holds post/put data for tests
        with open(path + '/refData/fixtures/ArticlePostData.json') as postData:
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
