from django.db import models


# Model to hold company Data
# Can also reference other companies that it owns
class Company(models.Model):
    name = models.CharField(max_length=50,unique=True)

    owns = models.ForeignKey('self',related_name='parent',blank=True,null=True)

    def __str__(self):
        return self.name

# Article is the base link to outside information
# an 'article' can actually be a report, journalism, or anything else relevant to our research
class Article(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField(unique=True)

    notes = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.title

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


# Model for our general categories
class EthicsCategory(models.Model):
    name = models.CharField(max_length=30,unique=True)

    def __str__(self):
        return self.name

# Model for the subcategories within those
class EthicsSubCategory(models.Model):
    category = models.ForeignKey(EthicsCategory,related_name='subcategories')

    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

# Custom Exception for CrossReference
class ChooseOneException(Exception):
    pass

# Single ethical factoid extracted from artical
class Factoid(models.Model):
    fact_type = models.CharField(max_length=300)
    value = models.CharField(max_length=50,blank=True,null=True)
    notes = models.TextField(blank=True,null=True)

    subcategory = models.ForeignKey(EthicsSubCategory, related_name='factoids')
    article = models.ForeignKey(Article, related_name='factoids')
    product = models.ForeignKey(Product, related_name='factoids',blank=True,null=True)
    company = models.ForeignKey(Company, related_name='factoids',blank=True,null=True)

    def __str__(self):
        return self.fact_type

    def save(self, *args, **kwargs):
        if self.product == None and self.company == None:
            raise ChooseOneException("You have to attach to either a Company or a Product")

        return super(CrossReference, self).save(*args, **kwargs)


