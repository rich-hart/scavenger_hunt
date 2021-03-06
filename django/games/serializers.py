from datetime import datetime, timezone, timedelta
from rest_framework import routers, serializers, viewsets
from rest_framework.validators import UniqueValidator
from .models import *



class PenaltySerializer(serializers.ModelSerializer):
    expires = serializers.DateTimeField()
    now = serializers.DateTimeField()
    remaining = serializers.IntegerField()
    def to_representation(self, instance):
        instance.now = datetime.now(timezone.utc)
        instance.expires = instance.created + timedelta(seconds=instance.duration)
        if instance.expires > instance.now:
            remaining = instance.expires - instance.now
            instance.remaining = remaining.seconds
        else:
            instance.remaining = 0
 
        data = super(PenaltySerializer, self).to_representation(instance)
        return data
 
    class Meta:
        model = Penalty
        fields = '__all__'
#        fields = ('id','expires','now')

class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__' 


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id',)


class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = ('id','verified','reward')
        depth = 2

class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = '__all__'

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
    def create(self, validated_data):
        problem_data = validated_data['problem']
        question_data = problem_data['question']
        question = Question.objects.create(
            text=question_data['text'],
            video=question_data['video'],
            picture=question_data['picture'],
        )
        solution_data = validated_data['solution']
        answer_data = solution_data['answer']
        answer = Answer.objects.create(
            text=answer_data['text'],
        )
        challenge = Challenge.objects.create(
            problem=question.problem_ptr,
            solution=answer.solution_ptr,
            game=validated_data['game'],
        )
        return challenge
    class Meta:
        model = Challenge
        fields = ('id','problem', 'solution','game','index')

class HiddenChallengeSerializer(serializers.ModelSerializer):
    problem = ProblemSerializer()
    class Meta:
        model = Challenge
        fields = ('id','problem')

class SolveSerializer(serializers.ModelSerializer):
    answer = serializers.CharField()
    class Meta:
        model = Solution
        fields = ('id','answer')
