from rest_framework import serializers

from profile.models import Preference, Question, Answer

class PreferenceSerializer(serializers.ModelSerializer):
    tag_type = serializers.StringRelatedField()

    class Meta:
        model = Preference
        fields = ('tag_type','preference','id')

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('question','supplement','id')

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('question','answer','id')

class QuestionAnswerSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('question','supplement','answers')


