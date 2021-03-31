from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id','user', 'nickname')
        read_only_fields = fields
#        depth = 2

class ProfileDeleteSerializer(serializers.ModelSerializer):
    confirmation = serializers.CharField(write_only=True) 
    class Meta:
        model = Profile
        fields = ('id','user', 'nickname','confirmation')
        read_only_fields = ('id','user', 'nickname')
        depth = 2
