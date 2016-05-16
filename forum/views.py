from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.auth import get_user_model
from django.db.models import Count, Max, Prefetch
from rest_framework import generics
from rest_framework import permissions

from .models import Thread, Post, Category
from .serializers import ThreadListSerializer, ThreadCreateSerializer, PostSerializer, CategoryListSerializer, \
        CategoryDetailSerializer, ThreadDetailSerializer, PostNewSerializer

User = get_user_model()

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all().prefetch_related(
            'threads',
            'threads__posts'
        ).annotate(
            thread_count=Count('threads')
        ).annotate(
            latest=Max('threads__posts__created_date')
        ).annotate(
            post_count=Count('threads__posts')
        )
    serializer_class = CategoryListSerializer


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all().prefetch_related(
            Prefetch('threads', queryset=Thread.objects.prefetch_related('posts').annotate(
                post_count=Count('posts')
            ).annotate(
                latest=Max('posts__created_date')
            ))
        )
    serializer_class = CategoryDetailSerializer


class ThreadNewView(generics.CreateAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadCreateSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request, *args, **kwargs):
         request.data['author'] = request.user.id
         return super(ThreadNewView,self).create(request,*args,**kwargs)


class ThreadDetailView(generics.RetrieveAPIView):
    queryset = Thread.objects.prefetch_related('posts', 'posts__author').all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = ThreadDetailSerializer


class PostNewView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostNewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
 
    def create(self, request, *args, **kwargs):
         request.data['author'] = request.user.id
         return super(PostNewView,self).create(request,*args,**kwargs)


