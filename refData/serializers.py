from rest_framework import serializers

from refData.models import Article, CrossReference

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title','url','notes')