from django.db import models
from django.contrib.auth.models import User

from refData.models import Article, Company, Product

# Model for our general categories
class EthicsCategory(models.Model):
    name = models.CharField(max_length=30,unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

# Model for the subcategories within those
class EthicsSubCategory(models.Model):
    category = models.ForeignKey(EthicsCategory,related_name='subcategories')

    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('category','name')

# Custom Exception for CrossReference
class ChooseOneException(Exception):
    pass

class TagType(models.Model):
    name = models.CharField(max_length=300)

    class Meta:
        abstract = True

# Potential types of Ethical Factoids
class EthicsType(TagType):
    subcategory = models.ForeignKey(EthicsSubCategory, related_name='tag_types')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

class MetaType(TagType):
    pass

class Tag(models.Model):
    article = models.ForeignKey(Article, related_name='%(class)ss')

    submitted_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User)

    class Meta:
        abstract = True

class EthicsTag(Tag):
    tag_type = models.ForeignKey(EthicsType)

    excerpt = models.TextField()

    value = models.DecimalField(max_digits=15,decimal_places=2,blank=True,null=True)

    product = models.ForeignKey(Product, related_name='tags',blank=True,null=True)
    company = models.ForeignKey(Company, related_name='tags')


    class Meta:
        unique_together = ('tag_type','article','company')
        ordering = ('article','tag_type')

    def __str__(self):
        return "{1} : {1}".format(tag_type,article)

class MetaTag(Tag):
    tag_type = models.ForeignKey(MetaType)

    class Meta:
        unique_together = ('tag_type','article')

