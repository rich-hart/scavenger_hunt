import re
from datetime import datetime, timezone
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions
from rest_framework.response import Response
from fuzzywuzzy import fuzz
import django_filters
from .serializers import *


ANSWER_THRESHOLD = 95
PENALTY_TIMER = 5 * 60

class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_staff and not isinstance(user, AnonymousUser)

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [ IsStaff | IsAdminUser ]


class AchievementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        player = self.request.user.profile.player
        achievements = Achievement.objects.filter(player=player)
        return achievements

class RewardViewSet(viewsets.ModelViewSet):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer
    permission_classes=[IsStaff | IsAdminUser]



class AwardViewSet(viewsets.ModelViewSet):
    serializer_class = AwardSerializer
    permission_classes=[IsAuthenticated]
    http_method_names = ['get', 'head','put']
    def get_queryset(self):
        player = self.request.user.profile.player
        awards = Award.objects.filter(player=player)
        return awards
 
class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    permission_classes = [ IsStaff | IsAdminUser ]
    filterset_fields = ['game']

    @action(
        detail=True,
        serializer_class=SolveSerializer,
        methods=['post','get'],
        permission_classes=[IsAuthenticated],
    ) 
    def solve(self, request,pk):
#        import ipdb; ipdb.set_trace()
        data = dict()
        challenge = self.get_object()
        player = request.user.profile.player
        achievement = Achievement.objects.filter(
            player=player,
            challenge=challenge,
        ).first()
        penalty = Penalty.objects.filter(
            game=challenge.game,
            player=player
        ).first()
        now = datetime.now()
        if achievement:
            data['msg']='Solved'
            response = Response(data)
            return response


        if not penalty:
            pass
        elif penalty.type=='red' and (now-penalty.created).seconds < PENALTY_TIMER:
            data['msg']='RED ALERT'
            data['penalty']='red'
            response = Response(data)
            return response

#        if penalties.filter(type='red'):
#            data['msg']=''
        if self.request.method == 'GET':
            data['msg']='post answer'
            response = Response(data)
            return response
        player_answer = str(self.request.data['answer']).lower()
        player_answer = ''.join(re.findall(r'[a-z]', player_answer))
        answer = challenge.solution.answer.text.lower()
        answer = ''.join(re.findall(r'[a-z]', answer))       
        if fuzz.ratio(player_answer,answer) > ANSWER_THRESHOLD:
            data['msg'] = 'Correct'
            Achievement.objects.create(
                player=player,
                challenge=challenge,
            )
        else:
            data['msg'] = 'Incorrect'
            if not penalty:
                penalty_type = 'general'
                Penalty.objects.create(
                    game=challenge.game,
                    player=player,
                    type=penalty_type,
                )
            elif penalty.type=='general':
                penalty.type='yellow'
                penalty.save()
            elif penalty_type=='yellow':
                penalty.type='red'
                penalty.save()
            data['penalty']=penalty_type
        response = Response(data)
        return response


    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated]) 
    def solved(self, request):
        player = request.user.profile.player
        achievement = Achievement.objects.filter(player=player)
        queryset = [ a.challenge for a in achievement]

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    @action(
        detail=False,
        methods=['get'],
        serializer_class=HiddenChallengeSerializer,
        permission_classes=[IsAuthenticated],
    ) 
    def unsolved(self, request):
        player = request.user.profile.player
        games = player.game_set.all()
        challenges = []
        for game in games:
            _challenges = game.challenges.all()
            challenges += _challenges
        achievement = Achievement.objects.filter(player=player)
        completed_challenges = set([ a.challenge for a in achievement])
        challenges = set(challenges)
        queryset = list(challenges - completed_challenges)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



          
