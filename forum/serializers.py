from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Thread, Post, Category
from common.serializers import LocalDateTimeField


User = get_user_model()


class CategoryListSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    thread_count = serializers.IntegerField()
    post_count = serializers.IntegerField()
    latest = LocalDateTimeField(format="%-I:%M%p %m/%d/%Y")

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'thread_count', 'latest', 'post_count')


class ThreadListSerializer(serializers.ModelSerializer):
    post_count = serializers.IntegerField()
    latest = LocalDateTimeField(format="%-I:%M%p %m/%d/%Y")
    created_date = LocalDateTimeField(format="%-I:%M%p %m/%d/%Y")
    author = serializers.StringRelatedField()

    class Meta:
        model = Thread
        fields = ('id', 'subject', 'post_count', 'latest', 'author', 'created_date')


class CategoryDetailSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    threads = ThreadListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'threads')


class ThreadCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Thread
        fields = ('subject', 'category', 'author')


class PostSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    author = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = ('id', 'author', 'created_date', 'text',
            'last_edited_date', 'thread',)


class ThreadDetailSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Thread
        fields = ('subject', 'author', 'posts')


class PostNewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('author', 'text', 'thread')
