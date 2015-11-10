from rest_framework import serializers

from profile.models import Preference

class PreferenceSerializer(serializers.ModelSerializer):
    tag_type = serializers.StringRelatedField()

    class Meta:
        model = Preference
        fields = ('tag_type','preference','id')
