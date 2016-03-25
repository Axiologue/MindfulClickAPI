from rest_framework import serializers

from .models import Post

class PostFullSerializer(serializers.ModelSerializer):
    posted_by = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = ('pub_time', 'posted_by', 'title', 'sub_title', 'body', 'title_url')


class PostListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('title', 'sub_title', 'id')
