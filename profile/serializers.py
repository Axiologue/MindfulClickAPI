from rest_framework import serializers
from django.contrib.auth import get_user_model

from profile.models import Preference, Question, Answer

User = get_user_model()

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

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'initial_answers', 'is_staff', 'email')
