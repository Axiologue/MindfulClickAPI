from rest_framework import serializers

from .models import Reference
from tags.serializers import EthicsTagSerializer

class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ('id','title','url','notes','added_by')


class ReferenceEthicsTagsSerializer(serializers.ModelSerializer):
    ethicstags = EthicsTagSerializer(read_only=True, many=True)
    added_by = serializers.StringRelatedField()

    class Meta:
        model = Reference
        fields = ('title','url','ethicstags','id','notes','added_by')


class ReferenceAllTagsSerializer(serializers.ModelSerializer):
    ethicstags = EthicsTagSerializer(read_only=True, many=True)
    added_by = serializers.StringRelatedField()
    metatags = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Reference
        fields = ('title','url','ethicstags','id','notes','added_by', 'metatags')


class ReferenceMetaTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ('title','url','metatags','id','notes','added_by')

