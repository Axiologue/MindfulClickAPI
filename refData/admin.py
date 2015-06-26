from import_export import resources, fields, widgets

from refData.models import Article, Product, Company

# Resource for importing CSV file of article
class ArticleResource(resources.ModelResource):

    class Meta:
        model = Article
        fields = ('title','url','notes')
        import_id_fields = ('url',)

# Resource for importing CSV file of company/brands
class CompanyResource(resources.ModelResource):
    name = fields.Field(column_name='Brand',attribute='name')

    class Meta:
        model = Company
        exclude = ('Scraping Status',)
        import_id_fields = ('name',)

# Resource for importing Product info
class ProductResource(resources.ModelResource):
    company = fields.Field(column_name='Brand',
                           attribute='company',
                           widget=widgets.ForeignKeyWidget(Company,'name'))
    price = fields.Field(column_name='Price ($)',attribute='price')
    image_link = fields.Field(column_name='Image Link',attribute='image_link')
    name = fields.Field(column_name='Name',attribute='name')
    division = fields.Field(column_name='Division',attribute='division')
    category = fields.Field(column_name='Category',attribute='category')

    class Meta:
        model = Product
        import_id_fields = ('name','division')
        fields = ('company','name','division','category','price','image_link')