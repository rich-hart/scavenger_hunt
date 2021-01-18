from rest_framework import routers, serializers, viewsets
from rest_framework.validators import UniqueValidator
from .models import *

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('text', 'video','picture')

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('text', )

class ProblemSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()
    class Meta:
        model = Problem
        fields = ('id','question', )

class SolutionSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer()
    class Meta:
        model = Solution
        fields = ('id','answer', )

class ChallengeSerializer(serializers.ModelSerializer):
    problem = ProblemSerializer()
    solution = SolutionSerializer()
    class Meta:
        model = Challenge
        fields = ('id','problem', 'solution')

