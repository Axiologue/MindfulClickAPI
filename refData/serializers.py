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

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name','id')

