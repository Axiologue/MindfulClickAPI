from django.http import Http404
from django.contrib.auth import get_user_model
from django.db.models import Count, Max, Prefetch
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Thread, Post, Category
from .serializers import ThreadListSerializer, ThreadCreateSerializer, PostSerializer, CategoryListSerializer, \
        CategoryDetailSerializer, ThreadDetailSerializer, PostNewSerializer

User = get_user_model()


class CategoryListView(generics.ListAPIView):
    """
    Returns all Categories
    Along with the Counts of Threads and Posts in each category
    """
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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CategoryDetailView(generics.RetrieveAPIView):
    """
    Returns a Single Category and all associated threads
    """
    queryset = Category.objects.all().prefetch_related(
            Prefetch('threads', queryset=Thread.objects.prefetch_related('posts').annotate(
                post_count=Count('posts')
            ).annotate(
                latest=Max('posts__created_date')
            ))
        )
    serializer_class = CategoryDetailSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ThreadNewView(generics.CreateAPIView):
    """
    Creates a new Thread and its first post
    """
    queryset = Thread.objects.all()
    serializer_class = ThreadCreateSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        request.data['author'] = request.user.id
        post_text = request.data.pop('post_content')

        # Save thread info 
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        thread = serializer.save()

        # Create first post
        Post(author=request.user, text=post_text, thread=thread).save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ThreadDetailView(generics.RetrieveAPIView):
    """
    Gets a single thread and all its associated posts
    """
    queryset = Thread.objects.prefetch_related('posts', 'posts__author').all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = ThreadDetailSerializer


class PostNewView(generics.CreateAPIView):
    """
    Creates a new post
    """
    queryset = Post.objects.all()
    serializer_class = PostNewSerializer
    permission_classes = (permissions.IsAuthenticated,)
 
    def create(self, request, *args, **kwargs):
         request.data['author'] = request.user.id
         return super(PostNewView,self).create(request,*args,**kwargs)


