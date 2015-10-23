from rest_framework import serializers

from profile.models import TagPref

class TagPrefSerializer(serializers.ModelSerializer):
    tag_type = serializers.StringRelatedField()

    class Meta:
        model = TagPref
        fields = ('tag_type','preference','id')
