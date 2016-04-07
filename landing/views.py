from rest_framework import generics

from drf_multiple_model.views import MultipleModelAPIView

from events.serializers import EventListSerializer
from events.models import Event
from blog.serializers import PostListSerializer
from blog.models import Post
from tags.serializers import EthicsTagListSerializer
from tags.models import EthicsTag


class RecentInfoView(MultipleModelAPIView):
    queryList = [
        (
            Post.objects.order_by('-pub_time').select_related('posted_by').all()[:5],
            PostListSerializer,
            'posts'
        ),
        (
            EthicsTag.objects.order_by('-submitted_at').select_related('company', 'product', 'reference', 'tag_type', 'added_by').all()[:5],
            EthicsTagListSerializer,
            'tags'
        ),
        (
            Event.objects.order_by('-start').select_related('location').all()[:5],
            EventListSerializer,
            'events'
        )
    ]
