from django.db import models

from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey


class ProductCategory(MPTTModel):
    name = models.CharField(max_length=255, db_index=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = ['name', 'parent']

    def __str__(self):
        return self.name


# Model to hold company Data
# Can also reference other companies that it owns
class Company(models.Model):
    name = models.CharField(max_length=50,unique=True)

    owned_by = models.ForeignKey('self', related_name='owns', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


def get_default_category():
    category, _ = ProductCategory.objects.get_or_create(name="Athletic Shoes")
    return category.id


class Product(models.Model):
    company = models.ForeignKey(Company, related_name='products')
    product_category = models.ForeignKey(ProductCategory, default=get_default_category, related_name="products")

    name = models.CharField(max_length=100)
    division = models.CharField(max_length=30,blank=True,null=True)
    category = models.CharField(max_length=40,blank=True,null=True)
    price = models.DecimalField(decimal_places=2,max_digits=7)

    image_link = models.URLField(max_length=350,blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('company','name')

