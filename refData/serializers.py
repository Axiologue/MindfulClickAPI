from rest_framework import serializers

from refData.models import Article, CrossReference

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

    class Meta:
        model = CrossReference
        fields = ('score','subcategory','notes')

class CrossByArticle(serializers.ModelSerializer):
    data = CrossSerializer(read_only=True)

    class Meta:
        model = Article
        fields = ('title','data')