from rest_framework import serializers

from refData.models import Article, CrossReference, Product, EthicsCategory, EthicsSubCategory, Company

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id','title','url','notes')

class ArticleNoIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title','url','notes')

class CrossSerializer(serializers.ModelSerializer):
    subcategory = serializers.StringRelatedField()
    company = serializers.StringRelatedField()
    product = serializers.StringRelatedField()

    class Meta:
        model = CrossReference
        fields = ('score','subcategory','notes','company','product')

class CrossCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrossReference
        fields = ('score','subcategory','notes','company','product','article')

class CrossByArticle(serializers.ModelSerializer):
    data = CrossSerializer(read_only=True, many=True)

    class Meta:
        model = Article
        fields = ('title','url','data','id','notes')

class ProductSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ('company','name','division','category','price')

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name','id')

class EthicsSubSerializer(serializers.ModelSerializer):
    class Meta:
        model = EthicsSubCategory
        fields = ('name','id')


class EthicsSerializer(serializers.ModelSerializer):
    subcategories = EthicsSubSerializer(read_only=True,many=True)

    class Meta:
        model = EthicsCategory
        fields = ('name','subcategories')