from import_export import resources, fields, widgets

from .models import Product, Company


# Resource for importing CSV file of company/brands
class CompanyResource(resources.ModelResource):
    name = fields.Field(column_name='Brand',attribute='name')

    class Meta:
        model = Company
        exclude = ('Scraping Status',)
        import_id_fields = ('name',)

# Resource for importing Product info
class ProductResource(resources.ModelResource):
    company = fields.Field(column_name='brand',
                           attribute='company',
                           widget=widgets.ForeignKeyWidget(Company,'name'))
    price = fields.Field(column_name='price',attribute='price')
    image_link = fields.Field(column_name='image_link',attribute='image_link')
    name = fields.Field(column_name='name',attribute='name')
    division = fields.Field(column_name='division',attribute='division')
    category = fields.Field(column_name='category',attribute='category')

    class Meta:
        model = Product
        import_id_fields = ('name','division')
        fields = ('company','name','division','category','price','image_link')
