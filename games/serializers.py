from rest_framework import routers, serializers, viewsets
from rest_framework.validators import UniqueValidator
from .models import *

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id','text', 'video','picture')

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id','text', )


