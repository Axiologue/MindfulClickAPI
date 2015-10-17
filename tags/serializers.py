from rest_framework import serializers

from tags.models import EthicsType, EthicsTag, EthicsSubCategory, MetaTag

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

class EthicsTagChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EthicsTag
        fields = ('tag_type','value','excerpt','company','product','article','id','added_by')

class EthicsSubSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    tag_types = EthicsTypeSerializer(read_only=True,many=True)

    class Meta:
        model = EthicsSubCategory
        fields = ('name','id','category','tag_types')

class MetaTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaTag
        fields = ('article','tag_type','added_by')
