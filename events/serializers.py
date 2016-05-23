from rest_framework import serializers

from .models import Event, Location
from common.serializers import LocalDateTimeField


class LocationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('name', 'city')


class LocationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('name', 'city', 'street_address', 'postal_code')


class EventListSerializer(serializers.ModelSerializer):
    location = LocationListSerializer()
    start = LocalDateTimeField()

    class Meta:
        model = Event
        fields = ('name', 'start', 'location', 'id', 'description')


class EventDetailSerializer(serializers.ModelSerializer):
    location = LocationDetailSerializer()
    start = LocalDateTimeField()
    end = LocalDateTimeField()

    class Meta:
        model = Event
        fields = ('name', 'start', 'location', 'id', 'end', 'description')
    
