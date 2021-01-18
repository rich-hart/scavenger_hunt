from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions
from rest_framework.response import Response
import django_filters
from .serializers import *

class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_staff and not isinstance(user, AnonymousUser)

class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    permission_classes = [ IsStaff | IsAdminUser ]
    filterset_fields = ['game']

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated]) 
    def unsolved(self, request):
        player = request.user.profile.player
        games = player.game_set.all()
        challenges = []
        for game in games:
            _challenges = game.challenges.all()
            challenges += _challenges
        achievement = Achievement.objects.filter(player=player)
        completed_challenges = set([ a.challenges for a in achievement])
        challenges = set(challenges)
        queryset = list(challenges - completed_challenges)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent_users, many=True)
        return Response(serializer.data)



           
