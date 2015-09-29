from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from rest_framework import status
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from refData.models import EthicsCategory, EthicsSubCategory, TagType, Tag, Article, Company
from refData.views import FormMetaView, ArticleNoTagView, ArticleWithCrossView, \
            NewArticleView, UpdateArticleView, NewTagView, UpdateTagView, NewTagTypeView

import json
import os

factory = APIRequestFactory()
from collections import OrderedDict


# Check that the article API endpoints are all functioning currently
class DataViewsTests(APITestCase):
    fixtures = ['refTestInput']

    maxDiff = None

    def setUp(self):
        path = os.environ['DJANGO_PATH']

        # instantiate client for testing actual URLS
        self.client = APIClient()

        # JSON file that holds the expect output of the tests
        # Also used in front end tests
        with open(path + '/refData/fixtures/refTestOutput.json') as data:
            self.output = json.load(data)

        # JSON file that holds post/put data for tests
        with open(path + '/refData/fixtures/refTestPostData.json') as postData:
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

    # Test for ArticleNoTagView
    # Expected data is a list of all articles that have no associated tags
    def test_article_no_tag_view(self):

        view = ArticleNoTagView.as_view()

        request = factory.get('/tags/articles/untagged/')

        with self.assertNumQueries(1):
            response = view(request).render()

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data, self.output[3])

    # Test ArticleNoTagView url endpoints
    def test_article_no_tag_view_url(self):
        response = self.client.get('/tags/articles/untagged/')

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data, self.output[3])

    # Test for ArticleWithCrossView
    # Expected data is a list of all tagged articles with their associated tags
    def test_article_with_cross_view(self):

        view = ArticleWithCrossView.as_view()

        request = factory.get('/tags/articles/tagged/')

        with self.assertNumQueries(4):
            response = view(request).render()

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data, self.output[5])

    # Test ArticleWithCrossView url endpoints
    def test_article_with_cross_view_url(self):
        response = self.client.get('/tags/articles/tagged/')

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data, self.output[5])

    # Test for NewArticleView
    # Accepts new Article data.  Returns the newly created Article
    def test_new_article_view(self):
        view = NewArticleView.as_view()

        # Confirm existing Article count
        self.assertEqual(Article.objects.count(),3)

        request = factory.post('/tags/articles/new/',self.postData[1])
        response = view(request).render()

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

        # Confirm that new Article is in database
        self.assertEqual(Article.objects.count(),4)

        #Check that the new Article is returned to the client
        self.assertEqual(response.data, self.output[7])

    # Test NewArticleView url endpoints
    def test_new_article_view_url(self):
        response = self.client.post('/tags/articles/new/',self.postData[1])

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

        request = factory.put('/tags/articles/2/',self.postData[3])
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
    def test_Edit_article_view_update(self):
        response = self.client.put('/tags/articles/2/',self.postData[3])

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data,self.output[9])

    # Test for same UpdateArticleView, but this time for deleting
    # Accepts just pk
    def test_edit_article_view_delete(self):
        # Confirm initial article count
        self.assertEqual(Article.objects.count(),3)

        view = UpdateArticleView.as_view()

        request = factory.delete('/tags/articles/2/')
        response = view(request,pk=2).render()

        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

        # Confirm article is no longer in database
        self.assertEqual(Article.objects.count(),2)
        with self.assertRaises(ObjectDoesNotExist):
            article = Article.objects.get(id=2)

    # Test UpdateArticleView delete endpoints
    def test_Edit_article_view_update(self):
        response = self.client.delete('/tags/articles/2/')

        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

    # Test for NewTagView
    # Accepts new Tag data.  Returns newly create Tag.
    def test_new_tag_view(self):
        # Confirm initial tag count
        self.assertEqual(Tag.objects.count(),1)

        # Confirm article in questions has no tags
        article = Article.objects.get(id=2)
        self.assertEqual(article.tags.count(),0)

        view = NewTagView.as_view()

        request = factory.post('/tags/tags/new/',self.postData[5])
        response = view(request).render()

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

        # Confirm new tag count
        self.assertEqual(Tag.objects.count(),2)

        # Confirm tag is on correct article
        article = Article.objects.get(id=2)
        self.assertEqual(article.tags.count(),1)
        tag = article.tags.all()[0]
        self.assertEqual(tag.id,3)

        # Confirm new Tag is returned to client
        self.assertEqual(response.data, self.output[11])

    # Test for NewTagView url endpoints
    def test_new_tag_view_url(self):
        response = self.client.post('/tags/tags/new/',self.postData[5])

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    # Test for UpdateTagView, changing existing Tag
    # Accepts new data for existing Tag.  Returns updated Tag
    def test_update_tag_view_changing_tag(self):
        # Confirm old data
        tag = Tag.objects.get(id=2)
        self.assertEqual(tag.excerpt,"Quote about Nike using carbon")
        self.assertEqual(tag.tag_type.id,4)

        view = UpdateTagView.as_view()

        request = factory.put('tags/tags/2/',self.postData[7])
        response = view(request,pk=2).render()

        self.assertEqual(response.status_code,status.HTTP_200_OK)

        # Confirm new Data
        tag = Tag.objects.get(id=2)
        self.assertEqual(tag.excerpt,"Different quote about Nike using carbon")

        # Confirm other data hasn't changed
        self.assertEqual(tag.tag_type.id,4)

        # Confirm that the updated Tag is returned to the client
        self.assertEqual(response.data,self.output[13])

    # Test for UpdateTagView put url endpoints
    def test_update_tag_view_changing_tag_url(self):
        response = self.client.put('/tags/tags/2/',self.postData[7])

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data,self.output[13])

    # Test for UpdateTagView, this time for deleting a Tag
    # Accepts just pk
    def test_update_tag_view_deleting_tag(self):
        # Confirm initial Tag count
        self.assertEqual(Tag.objects.count(),1)

        view = UpdateTagView.as_view()

        request = factory.delete('/tags/tags/2/')
        response = view(request,pk=2).render()

        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

        # Confirm Tag is no longer in the database
        self.assertEqual(Tag.objects.count(),0)
        with self.assertRaises(ObjectDoesNotExist):
            tag = Tag.objects.get(id=2)

    # Test UpdateTagView delete url endpoints
    def test_update_tag_view_deleting_tag_url(self):
        response = self.client.delete('/tags/tags/2/')

        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

    # Test for NewTagTypeView
    # Accepts data for new TagType, returns new created TagType
    def test_new_tag_type_view(self):
        # Confirm Initial TagType count
        self.assertEqual(TagType.objects.count(),5)

        # Confirm inital per subcategory TagType count
        subcat = EthicsSubCategory.objects.get(id=2)
        self.assertEqual(subcat.tag_types.count(),1)

        view = NewTagTypeView.as_view()

        request = factory.post('/tags/tag-types/new/',self.postData[9])
        response = view(request).render()

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

        # Confirm new TagType count
        self.assertEqual(TagType.objects.count(),6)

        # Confirm new per subcategory TagType count
        subcat = EthicsSubCategory.objects.get(id=2)
        self.assertEqual(subcat.tag_types.count(),2)

        self.assertEqual(response.data,self.output[15])

    # Test for NewTagTypeView url endpoing
    def test_new_tag_type_view_url(self):
        response = self.client.post('/tags/tag-types/new/',self.postData[9])

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)





        