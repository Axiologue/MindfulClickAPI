from rest_framework import generics 

from .models import Post
from .serializers import PostFullSerializer, PostListSerializer

class AllPostsView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class RecentPostsView(generics.ListAPIView):
    queryset = Post.objects.order_by('-pub_time').all()[:5]
    serializer_class = PostListSerializer


class PostView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostFullSerializer
    
