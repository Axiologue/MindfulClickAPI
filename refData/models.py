from django.db import models

# Model to hold company Data
# Can also reference other companies that it owns
class Company(models.Model):
    name = models.CharField(max_length=50,unique=True)

    owns = models.ForeignKey('self',related_name='parent')

    def __str__(self):
        return self.name

# Article is the base link to outside information
# an 'article' can actually be a report, journalism, or anything else relevant to our research
class Article(models.Model):
    tilte = models.CharField(max_length=200)
    url = models.URLField()

    description = models.TextField()

# Model to hold product info
class Product(models.Model):
    Company = models.ForeignKey(Company,related_name='products')

    DIVISIONS = (
        ('M','Men'),
        ('W','Women'),
        ('U','Unisex'),
        ('K','Kids'),
        ('P','Preschool'),
        ('I','Infant/Toddler'),
        ('B','Boys'),
        ('G','Girls'),
    )

    name = models.CharField(max_length=50,unique=True)
    division = models.CharField(max_length=1,choices=DIVISIONS,blank=True,null=True)
    category = models.CharField(max_length=30)
    price = models.DecimalField(decimal_places=2,max_digits=7)

    image_link = models.URLField()

    def __str__(self):
        return self.name

# Model for our general categories
class EthicsCategory(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

# Model for the subcategories within those
class EthicsSubCategory(models.Model):
    category = models.ForeignKey(EthicsCategory,related_name='subcategories')

    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

# Main link cross-referencing articles, Products, and Companies
class CrossReference(models.Model):
    VALUES = ((-5,'-5'),
              (-4,'-4'),
              (-3,'-3'),
              (-2,'-2'),
              (-1,'-1'),
              (1,'1'),
              (2,'2'),
              (3,'3'),
              (4,'4'),
              (5,'5'),)

    score = models.SmallIntegerField(choices=VALUES,blank=False,default=0)

    subcategory = models.ForeignKey(EthicsSubCategory, related_name='data')

    article = models.ManyToManyField(Article, related_name='data')