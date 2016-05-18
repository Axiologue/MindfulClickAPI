from rest_framework import serializers

from .models import Event, Location
from common.serializers import LocalDateTimeField


class LocationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('name', 'city')


class EventListSerializer(serializers.ModelSerializer):
    location = LocationListSerializer()
    start = LocalDateTimeField(format="%-I:%M%p %m/%d/%Y")

    class Meta:
        model = Event
        fields = ('name', 'start', 'location', 'id')
