from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from django.contrib.auth.models import AnonymousUser
from .serializers import *

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    def get_queryset(self):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return []
        return Profile.objects.filter(owner=user)
    
