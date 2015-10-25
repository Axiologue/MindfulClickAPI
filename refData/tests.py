from rest_framework.test import APITestCase, APIRequestFactory, APIClient, force_authenticate
from rest_framework import status
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from refData.views import ArticleNoTagView, ArticleWithCrossView, NewArticleView, UpdateArticleView, \
        ArticleNoDataView
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




        
