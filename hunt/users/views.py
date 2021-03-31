from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from django.contrib.auth.models import AnonymousUser
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import *

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProfileSerializer
    def get_queryset(self):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return []
        return [user.profile]
    
    @action(detail=False, methods=['post','get'], serializer_class=ProfileDeleteSerializer)
    def remove_user(self, request):
        """
        To delete your user profile type 'confirm' and then 'POST'.
        """
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Response([])
        if request.method == 'GET':
            serializer = ProfileSerializer(instance=user.profile)
            return Response(serializer.data)
        if request.method == 'POST':
            if request.data.get('confirmation').lower() == 'confirm':
                self.request.user.delete()
                return Response({'msg':'user deleted'})
            else:
                return Response({'msg':"please type 'confirm' to delete user"})

            
