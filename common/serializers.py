from rest_framework import serializers
from django.utils import timezone


# With thanks to: 
# http://stackoverflow.com/questions/17331578/django-rest-framework-timezone-aware-renderers-parsers
class LocalDateTimeField(serializers.DateTimeField):

    def to_representation(self, value):
        value = timezone.localtime(value)
        return super(LocalDateTimeField, self).to_representation(value)
