from django.db import models

from django.contrib.auth.models import User


# Model to hold company Data
# Can also reference other companies that it owns
class Company(models.Model):
    name = models.CharField(max_length=50,unique=True)

    owns = models.ForeignKey('self',related_name='parent',blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

# Article is the base link to outside information
# an 'article' can actually be a report, journalism, or anything else relevant to our research
class Article(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField(unique=True)

    notes = models.TextField(blank=True,null=True)

    pub_date = models.DateTimeField(blank=True,null=True)
    add_date = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('add_date',)

# Model to hold product info
class Product(models.Model):
    company = models.ForeignKey(Company,related_name='products')

    name = models.CharField(max_length=100)
    division = models.CharField(max_length=30,blank=True,null=True)
    category = models.CharField(max_length=40,blank=True,null=True)
    price = models.DecimalField(decimal_places=2,max_digits=7)

    image_link = models.URLField(max_length=350)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name','division')
        ordering = ('company','name')

