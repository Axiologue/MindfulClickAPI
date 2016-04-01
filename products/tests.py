from rest_framework.test import APITestCase, APIRequestFactory, APIClient, force_authenticate
from rest_framework import status
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

from .views import ProductListView, ProductNewView

import json
import os

factory = APIRequestFactory()

User = get_user_model()

# Check that the article API endpoints are all functioning currently
class ProductViewsTests(APITestCase):
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

    # Test ProductListView
    def test_product_list_view(self):
        view = ProductListView.as_view()

        # test unfiltered version
        request = factory.get('/articles/products/list/')
        response = view(request).render()

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data, self.output[27])

    # Test ProductListView
    def test_product_list_view_filtered(self):
        view = ProductListView.as_view()

        # test filtered version
        request = factory.get('/articles/products/list/?company_id=1&name=run',{'company_id':'1',"name":"run"})
        response = view(request).render()

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data, self.output[29])

    # Test ProductListView as endpoint
    def test_product_list_view_url(self):
        response = self.client.get('/articles/products/list/')

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data, self.output[27])

    def test_product_list_view_filtered_url(self):
        response = self.client.get('/articles/products/list/?company_id=1&name=run')

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data, self.output[29])


    # Test ProductNewView, with all possible fields
    def test_product_new_view(self):
        view = ProductNewView.as_view()

        request = factory.post('/products/new/',{
            "name": "Classic Runners",
            "company": 1,
            "division": "Men",
            "category": "Running",
            "price": 89.00,
            "image_link": "http://link.to/image.jpg"
        })
        force_authenticate(request, user=self.user)
        response = view(request).render()

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data,{
            "name": "Classic Runners",
            "company": 1,
            "division": "Men",
            "category": "Running",
            "price": "89.00",
        })

    # Test ProductNewView, with most restricted data
    def test_product_new_view(self):
        view = ProductNewView.as_view()

        request = factory.post('/products/new/',{
            "name": "Classic Runners",
            "company": 1,
            "price": 89.00,
        })
        force_authenticate(request, user=self.user)
        response = view(request).render()

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data,{
            "name": "Classic Runners",
            "company": 1,
            "price": "89.00",
        })
