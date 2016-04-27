from django.db import models
from django.conf import settings

from references.models import Reference
from products.models import Product, Company

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
    reference = models.ForeignKey(Reference, related_name='%(class)ss')

    submitted_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        abstract = True

# Custom Exception for CrossReference
class ChooseOneException(Exception):
        pass

class EthicsTag(Tag):
    tag_type = models.ForeignKey(EthicsType)

    excerpt = models.TextField()

    value = models.DecimalField(max_digits=15,decimal_places=2,blank=True,null=True)

    product = models.ForeignKey(Product, related_name='tags', blank=True, null=True)
    company = models.ForeignKey(Company, related_name='tags')


    class Meta:
        ordering = ('reference','tag_type')

    def __str__(self):
        return "{0} : {1}".format(self.tag_type, self.reference)


class MetaTag(Tag):
    tag_type = models.ForeignKey(MetaType)

    class Meta:
        unique_together = ('tag_type','reference')

    def __str__(self):
        return self.tag_type.name

