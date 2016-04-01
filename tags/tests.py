from rest_framework.test import APITestCase, APIRequestFactory, APIClient, force_authenticate
from rest_framework import status
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

from .views import FormMetaView, NewEthicsTagView, UpdateEthicsTagView, NewEthicsTypeView, \
        NoRelDataView, UpdateMetaTagView
from .models import EthicsType, EthicsTag, EthicsSubCategory, MetaTag
from references.models import Reference

import os
import json

User = get_user_model()

factory = APIRequestFactory()

# Check that the article API endpoints are all functioning currently
class TagViewsTests(APITestCase):
    fixtures = ['AuthTest','ReferenceTestInput','TestCategories','TestCompanies','TestTags']

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
        with open(path + '/references/fixtures/ReferenceTestOutput.json') as data:
            self.output = json.load(data)

        # JSON file that holds post/put data for tests
        with open(path + '/references/fixtures/ReferencePostData.json') as postData:
            self.postData = json.load(postData)

    # Test for FormMetaView
    # Expected Data is a list of companies and a list of Ethics Categories (with associated tag types)
    def test_form_meta_view(self):
        view = FormMetaView.as_view()

        request = factory.get('/tags/formMeta/')

        with self.assertNumQueries(3):
            response = view(request).render()

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data,self.output[1])

    # Testing FormMetaView url endpoints
    def test_form_meta_view_url(self):
        response = self.client.get('/tags/formMeta/')

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data,self.output[1])

    # Test for NewEthicsTagView
    # Accepts new EthicsTag data.  Returns newly create Tag.
    def test_new_ethics_tag_view(self):
        # Confirm initial tag count
        self.assertEqual(EthicsTag.objects.count(),1)

        # Confirm article in questions has no tags
        article = Reference.objects.get(id=2)
        self.assertEqual(article.ethicstags.count(),0)

        view = NewEthicsTagView.as_view()

        request = factory.post('/tags/etags/new/',self.postData[5])
        force_authenticate(request, user=self.user)
        response = view(request).render()

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

        # Confirm new tag count
        self.assertEqual(EthicsTag.objects.count(),2)

        # Confirm tag is on correct article
        article = Reference.objects.get(id=2)
        self.assertEqual(article.ethicstags.count(),1)
        tag = article.ethicstags.all()[0]
        self.assertEqual(tag.id,4)

        # Confirm new Tag is returned to client
        self.assertEqual(response.data, self.output[11])

    # Test for NewEthicsTagView url endpoints
    def test_new_ethcs_tag_view_url(self):
        response = self.client.post('/tags/etags/new/',self.postData[5])

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    # Test for UpdateTagView, changing existing Tag
    # Accepts new data for existing EthicsTag.  Returns updated EthicsTag
    def test_update_ethics_tag_view_changing_tag(self):
        # Confirm old data
        tag = EthicsTag.objects.get(id=2)
        self.assertEqual(tag.excerpt,"Quote about Nike using carbon")
        self.assertEqual(tag.tag_type.id,4)

        view = UpdateEthicsTagView.as_view()

        request = factory.put('tags/etags/2/',self.postData[7])
        force_authenticate(request, user=self.user)
        response = view(request,pk=2).render()

        self.assertEqual(response.status_code,status.HTTP_200_OK)

        # Confirm new Data
        tag = EthicsTag.objects.get(id=2)
        self.assertEqual(tag.excerpt,"Different quote about Nike using carbon")

        # Confirm other data hasn't changed
        self.assertEqual(tag.tag_type.id,4)

        # Confirm that the updated Tag is returned to the client
        self.assertEqual(response.data,self.output[13])

    # Test for UpdateEthicsTagView put url endpoints
    def test_update_ethics_tag_view_changing_tag_url(self):
        response = self.client.put('/tags/etags/2/',self.postData[7])

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data,self.output[13])

    # Test for UpdateEthicsTagView, this time for deleting a EthicsTag
    # Accepts just pk
    def test_update_ethics_tag_view_deleting_tag(self):
        # Confirm initial EthicsTag count
        self.assertEqual(EthicsTag.objects.count(),1)

        view = UpdateEthicsTagView.as_view()

        request = factory.delete('/tags/etags/2/')
        force_authenticate(request, user=self.user)
        response = view(request,pk=2).render()

        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

        # Confirm EthicsTag is no longer in the database
        self.assertEqual(EthicsTag.objects.count(),0)
        with self.assertRaises(ObjectDoesNotExist):
            tag = EthicsTag.objects.get(id=2)

    # Test UpdateEthicsTagView delete url endpoints
    def test_update_ethics_tag_view_deleting_tag_url(self):
        response = self.client.delete('/tags/etags/2/')

        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

    # Test for NewEthicsTagTypeView
    # Accepts data for new EthicsType, returns new created EthicsType
    def test_new_ethics_type_view(self):
        # Confirm Initial EthicsType count
        self.assertEqual(EthicsType.objects.count(),5)

        # Confirm inital per subcategory EthicsType count
        subcat = EthicsSubCategory.objects.get(id=2)
        self.assertEqual(subcat.tag_types.count(),1)

        view = NewEthicsTypeView.as_view()

        request = factory.post('/tags/etypes/new/',self.postData[9])
        force_authenticate(request, user=self.user)
        response = view(request).render()

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

        # Confirm new EthicsType count
        self.assertEqual(EthicsType.objects.count(),6)

        # Confirm new per subcategory EthicsType count
        subcat = EthicsSubCategory.objects.get(id=2)
        self.assertEqual(subcat.tag_types.count(),2)

        self.assertEqual(response.data,self.output[15])

    # Test for NewEthicsTypeView url endpoing
    def test_new_ethics_type_view_url(self):
        response = self.client.post('/tags/etypes/new/',self.postData[9])

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    # Test for NoRelDataView
    # Accepts article, and marks the article as no relevant Data
    def test_no_rel_data_view(self):
        # Confirm Iniital MetaTag count
        self.assertEqual(MetaTag.objects.count(),1)

        view = NoRelDataView.as_view()

        request = factory.post('/tags/mtags/new/',self.postData[11])
        force_authenticate(request, user=self.user)
        response = view(request).render()

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

        # Confirm new MetaTag count
        self.assertEqual(MetaTag.objects.count(),2)

        # Confirm returned data
        self.assertEqual(response.data,self.output[19])

    # Test for NoRelDataView url endpoint
    def test_no_rel_data_view_url(self):
        response = self.client.post('/tags/mtags/new/',self.postData[11])

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    # Test for UpdateMetaTagView tag deletion
    # Takes an MetaTag id, deletes it
    def test_update_meta_tag_view_delete(self):
        # Confirm initial MetaTag count
        self.assertEqual(MetaTag.objects.count(),1)

        view = UpdateMetaTagView.as_view()

        request = factory.delete('/tags/mtags/1/')
        force_authenticate(request, user=self.user)
        response = view(request,pk=1).render()

        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

        # Confirm MetaTag is no longer in the database
        self.assertEqual(MetaTag.objects.count(),0)
        with self.assertRaises(ObjectDoesNotExist):
            tag = EthicsTag.objects.get(id=1)
