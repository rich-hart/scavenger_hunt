from django.test import TestCase
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate

from .views import *

class PlayerTest(TestCase):
    def test_model(self):
        user = User.objects.create()
        self.assertTrue(user.profile.player)

class GameTest(APITestCase):
    def tearDown(self):
        User.objects.all().delete()

    def test_model(self):
        self.user = User.objects.create()
        self.game = Game.objects.create()
        self.assertFalse(self.game.players.all())
        self.game.players.add(self.user.profile.player)
        self.game.save()
        self.assertTrue(self.game.players.all())

    def test_challenge_model(self):
        self.test_model()
        question = Question.objects.create(text='True')
        answer = Answer.objects.create(text='True')
        self.challenge = Challenge(
            problem=question,
            solution=answer,
            game=self.game,
        )

    def test_challenge_list_view(self):
        self.test_challenge_model()
        self.challenge.game.players.add(self.user.profile.player)
        self.challenge.save()
        url = reverse('challenge-list')
        self.client.force_login(self.user)
        response = self.client.get(url, format='json')
        self.assertEqual(str(response.data['detail']),'You do not have permission to perform this action.')
        staff = User.objects.create(is_staff=True,username='staff') 
        self.client.force_login(staff)
        response = self.client.get(url, format='json')
        self.assertTrue(response.data['count']) 

    def test_challenge_unsolved_view(self):
        self.test_challenge_model()
        self.challenge.game.players.add(self.user.profile.player)
        self.challenge.save()
        url = reverse('challenge-unsolved')
        self.client.force_login(self.user)
        response = self.client.get(url, format='json')
        self.assertTrue(response.data['count'])


