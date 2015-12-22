from rest_framework import serializers

from refData.models import Article, Product, Company
from tags.serializers import EthicsTagSerializer

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id','title','url','notes','added_by')


class ArticleEthicsTagsSerializer(serializers.ModelSerializer):
    ethicstags = EthicsTagSerializer(read_only=True, many=True)

    class Meta:
        model = Article
        fields = ('title','url','ethicstags','id','notes','added_by')

class ArticleMetaTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title','url','metatags','id','notes','added_by')

class ProductSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ('company','name','division','category','price')

class NewProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('company','name','price')

    # Modified init function to add optional fields if they're in the data set
    def __init__(self, *args, **kwargs):
        self.Meta.fields = list(self.Meta.fields)

        data = kwargs.get('data')

        if data:
            fields = list(data.keys())
            for f in ['image_url','division','category']:
                if f in fields:
                    self.Meta.fields.append(f)

        super(NewProductSerializer, self).__init__(*args,**kwargs)


class ProductSimpleSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ('name','id','company')

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name','id')

