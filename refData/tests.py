from rest_framework.test import APITestCase, APIRequestFactory, APIClient, force_authenticate
from rest_framework import status
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from refData.views import ArticleNoTagView, ArticleWithCrossView, NewArticleView, UpdateArticleView, \
        ArticleNoDataView, ProductListView, ProductFetchView, ProductNewView
from refData.models import Article

import json
import os

factory = APIRequestFactory()


# Check that the article API endpoints are all functioning currently
class ArticleViewsTests(APITestCase):
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



    # Test for ArticleNoTagView
    # Expected data is a list of all articles that have no associated tags
    def test_article_no_tag_view(self):

        view = ArticleNoTagView.as_view()

        request = factory.get('/articles/articles/untagged/')

        with self.assertNumQueries(1):
            response = view(request).render()

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data, self.output[3])

    # Test ArticleNoTagView url endpoints
    def test_article_no_tag_view_url(self):
        response = self.client.get('/articles/articles/untagged/')

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data, self.output[3])

    # Test for ArticleWithCrossView
    # Expected data is a list of all tagged articles with their associated tags
    def test_article_with_cross_view(self):

        view = ArticleWithCrossView.as_view()

        request = factory.get('/articles/articles/tagged/')

        with self.assertNumQueries(4):
            response = view(request).render()
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data, self.output[5])

    # Test ArticleWithCrossView url endpoints
    def test_article_with_cross_view_url(self):
        response = self.client.get('/articles/articles/tagged/')

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data, self.output[5])

    # Test for NewArticleView
    # Accepts new Article data.  Returns the newly created Article
    def test_new_article_view(self):
        view = NewArticleView.as_view()

        # Confirm existing Article count
        self.assertEqual(Article.objects.count(),4)

        request = factory.post('/articles/articles/new/',self.postData[1])
        force_authenticate(request, user=self.user)
        response = view(request).render()

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

        # Confirm that new Article is in database
        self.assertEqual(Article.objects.count(),5)

        #Check that the new Article is returned to the client
        self.assertEqual(response.data, self.output[7])

    # Test NewArticleView url endpoints
    def test_new_article_view_url(self):
        response = self.client.post('/articles/articles/new/',self.postData[1])

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    # Test for UpdateArticleView, changing article
    # Accepts new data for existing Article.  Returns altered Article
    def test_edit_article_view_update(self):

        # Confirm old data
        article = Article.objects.get(id=2)
        self.assertEqual(article.title,"Adidas Workers Rights")
        self.assertEqual(article.notes,"Fictional Article Regarding Worker Safety")
        self.assertEqual(article.url,"http://www.adidas-group.com/en/workersaftey")

        view = UpdateArticleView.as_view()

        request = factory.put('/articles/articles/2/',self.postData[3])
        force_authenticate(request, user=self.user)
        response = view(request, pk=2).render()

        self.assertEqual(response.status_code,status.HTTP_200_OK)

        # Check that the updated Article is returned to the client
        self.assertEqual(response.data,self.output[9])

        # Confirm new Data
        article = Article.objects.get(id=2)
        self.assertEqual(article.title,"New Balance Workers Rights")
        self.assertEqual(article.notes,"Fictional Article Regarding Worker Safety.  Updated from Adidas to New Balance")

        # Confirm URL is unchanged
        self.assertEqual(article.url,"http://www.adidas-group.com/en/workersaftey")

    # Test UpdateArticleView put endpoints
    def test_edit_article_view_update_edit(self):
        response = self.client.put('/articles/articles/2/',self.postData[3])

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data,self.output[9])

    # Test for same UpdateArticleView, but this time for deleting
    # Accepts just pk
    def test_edit_article_view_delete(self):
        # Confirm initial article count
        self.assertEqual(Article.objects.count(),4)

        view = UpdateArticleView.as_view()

        request = factory.delete('/articles/articles/2/')
        force_authenticate(request, user=self.user)
        response = view(request,pk=2).render()

        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

        # Confirm article is no longer in database
        self.assertEqual(Article.objects.count(),3)
        with self.assertRaises(ObjectDoesNotExist):
            article = Article.objects.get(id=2)

    # Test UpdateArticleView delete endpoints
    def test_Edit_article_view_update(self):
        response = self.client.delete('/articles/articles/2/')

        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

    # Test for ArticleNoDataView
    # Expected data is a list of all articles that have been marker irrelevant
    def test_article_no_data_tag_view(self):

        view = ArticleNoDataView.as_view()

        request = factory.get('/articles/articles/noData/')

        with self.assertNumQueries(2):
            response = view(request).render()
       
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data, self.output[17])

    # Test ArticleNoDataView url endpoints
    def test_article_no_data_tag_view_url(self):
        response = self.client.get('/articles/articles/noData/')

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data, self.output[17])

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
