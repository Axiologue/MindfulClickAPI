from rest_framework import serializers
from forum.models import Thread, Post
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class ThreadSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Thread
        fields = ('id', 'subject',)


class PostSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'created_date', 'text',
            'last_edited_date', 'thread',)


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'posts')

