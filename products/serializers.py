from rest_framework import serializers

from .models import Product, Company, ProductCategory


class ProductSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ('company', 'name', 'category', 'price', )


class NewProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('company', 'name', 'price', )

    # Modified init function to add optional fields if they're in the data set
    def __init__(self, *args, **kwargs):
        self.Meta.fields = list(self.Meta.fields)

        data = kwargs.get('data')

        if data:
            fields = list(data.keys())
            for f in ['image_url', 'division', 'category']:
                if f in fields:
                    self.Meta.fields.append(f)

        super(NewProductSerializer, self).__init__(*args,**kwargs)


class ProductSimpleSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ('name', 'id', 'company', )


class CompanySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name', )


class CompanySerializer(serializers.ModelSerializer):
    owned_by = serializers.StringRelatedField()
    owns = serializers.StringRelatedField(many=True)

    class Meta:
        model = Company
        fields = ('name', 'id', 'owns', 'owned_by', )


class ProductCategory(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('name', 'parent', 'id', )
