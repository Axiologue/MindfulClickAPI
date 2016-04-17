from rest_framework import serializers

from .models import EthicsType, EthicsTag, EthicsSubCategory, MetaTag, EthicsCategory
from references.models import Reference


class EthicsTypeSerializer(serializers.ModelSerializer):
    subcategory = serializers.StringRelatedField()

    class Meta:
        model = EthicsType
        fields = ('name','subcategory','id')


class EthicsTypeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EthicsType
        fields = ('name','subcategory','id')


class EthicsTagSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()
    product = serializers.StringRelatedField()
    tag_type = EthicsTypeSerializer()

    class Meta:
        model = EthicsTag
        fields = ('tag_type','value','excerpt','company','product','id','added_by')


class EthicsTagListSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()
    product = serializers.StringRelatedField()
    tag_type = serializers.StringRelatedField()
    reference = serializers.StringRelatedField()
    added_by = serializers.StringRelatedField()

    class Meta:
        model = EthicsTag
        fields = ('tag_type', 'product', 'company', 'value', 'id', 'added_by', 'submitted_at', 'reference')


class EthicsTagChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EthicsTag
        fields = ('tag_type','value','excerpt','company','product','reference','id','added_by')


class ReferenceShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ('title', 'url', 'id', 'notes')


class EthicsTagByObjectSerializer(serializers.ModelSerializer):
    tag_type = serializers.StringRelatedField()
    added_by = serializers.StringRelatedField()
    submitted_at = serializers.DateTimeField(format="%-I:%M%p %m/%d/%Y")
    reference = ReferenceShortSerializer(read_only=True)
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj.tag_type.subcategory.category.name

    class Meta:
        model = EthicsTag
        field = ('tag_type', 'value', 'excerpt', 'reference', 'added_by', 'submitted_at', 'category')


class EthicsSubSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    tag_types = EthicsTypeSerializer(read_only=True,many=True)

    class Meta:
        model = EthicsSubCategory
        fields = ('name','id','category','tag_types')


class MetaTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaTag
        fields = ('reference','tag_type','added_by')
