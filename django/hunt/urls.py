"""hunt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from rest_framework.decorators import api_view
from django.shortcuts import redirect
from django.contrib.auth import logout


from users.views import *
from games.views import *

router = routers.DefaultRouter()
router.register(r'profile', ProfileViewSet, basename='profile')
router.register(r'users', UserViewSet)
router.register(r'games', GameViewSet)
router.register(r'challenges', ChallengeViewSet, basename='challenge')
router.register(r'awards', AwardViewSet, basename='award')
router.register(r'rewards', RewardViewSet)
router.register(r'achievements', AchievementViewSet, basename='achievement')
router.register(r'penalties', PenaltyViewSet, basename='penalty')

@api_view(['GET'])
def home(request):
    return redirect('api-root')



urlpatterns = [
    path('admin/', admin.site.urls),
#    path('', home),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include(router.urls)),
#    path('api/logout/', logout_view),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include('social_django.urls', namespace='social')),

]
