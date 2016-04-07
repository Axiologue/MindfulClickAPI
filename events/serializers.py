from rest_framework import serializers

from .models import Event, Location


class LocationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('name', 'city')


class EventListSerializer(serializers.ModelSerializer):
    location = LocationListSerializer()

    class Meta:
        model = Event
        fields = ('name', 'start', 'location', 'id')
