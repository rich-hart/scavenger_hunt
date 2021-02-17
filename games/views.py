import math
import re
from datetime import datetime, timezone, timedelta
from django.conf import settings
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




class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_staff and not isinstance(user, AnonymousUser)

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [ IsStaff | IsAdminUser ]


class PenaltyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PenaltySerializer
    permission_classes=[IsAuthenticated]
    http_method_names = ['get', 'head']
    def get_queryset(self):
        player = self.request.user.profile.player
        penalties = Penalty.objects.filter(player=player)
        return penalties

class AchievementViewSet(viewsets.ReadOnlyModelViewSet):
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
        data = dict()
        challenge = self.get_object()
        player = request.user.profile.player
        now = datetime.now(timezone.utc)

        achievement = Achievement.objects.filter(
            player=player,
            challenge=challenge,
        ).first()
        
        penalties = Penalty.objects.filter(
            created__gte = (now - timedelta(seconds=settings.PENALTY_TIMER)),
            game=challenge.game,
            player=player,
        )        

        if achievement:
            data['msg']='Solved'
            data['state'] = 'solved'
            response = Response(data)
            return response 

        if not penalties:
            pass
        elif penalties.filter(type='red'):
            data['msg']=f'RED ALERT'
            data['penalty']='red'
            data['state'] = 'penalty'
            response = Response(data)
            return response

        if self.request.method == 'GET':
            data['msg']='post answer'
            response = Response(data)
            return response

        player_answer = str(self.request.data['answer']).lower()
        player_answer = ''.join(re.findall(r'[a-z]', player_answer))
        answer = challenge.solution.answer.text.lower()
        answer = ''.join(re.findall(r'[a-z]', answer))       
        if fuzz.ratio(player_answer,answer) > settings.ANSWER_THRESHOLD:
            data['msg'] = 'Correct'
            data['state'] = 'solved'
            Achievement.objects.create(
                player=player,
                challenge=challenge,
            )
        else:
            data['msg'] = 'Incorrect'
            if not penalties:
                penalty = Penalty.objects.create(
                    game=challenge.game,
                    player=player,
                    type='general',
                )
            elif penalties.filter(type='yellow'):
                penalty = Penalty.objects.create(
                    game=challenge.game,
                    player=player,
                    type='red',
                )
            elif penalties.filter(type='general'):
                penalty = Penalty.objects.create(
                    game=challenge.game,
                    player=player,
                    type='yellow',
                )

            data['penalty']=penalty.type
            data['state'] = 'penalty'
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



          
