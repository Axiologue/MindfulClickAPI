from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.auth import get_user_model
from django.db.models import Count, Max
from rest_framework import generics
from rest_framework import permissions

from .models import Thread, Post, Category
from .serializers import ThreadListSerializer, ThreadCreateSerializer, PostSerializer, CategoryListSerializer, \
        CategoryDetailSerializer

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
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer


class ThreadListView(generics.ListAPIView):
    serializer_class = ThreadListSerializer

    def get_queryset(self):
        queryset = Thread.objects.all()
        try:
            category = Category.objects.get(id=self.kwargs.get('pk', None))
            queryset = queryset.filter(category=category)
        except Category.DoesNotExist:
            raise Http404("No Matching Category Found")

        queryset = queryset.prefetch_related('posts').annotate(
                post_count=Count('posts')
            ).annotate(
                latest=Max('posts__created_date')
            )

        return queryset


class ThreadNewView(generics.CreateAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadCreateSerializer

    def create(self, request, *args, **kwargs):
         request.data['author'] = request.user.id
         return super(ThreadNewView,self).create(request,*args,**kwargs)


class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = self.queryset 
        try:
            thread = Thread.objects.get(id=self.request.kwargs.get('pk', None))
            queryset = queryset.filter(category=category)
        except Category.DoesNotExist:
            raise Http404("No Matching Category Found")
        return queryset


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
