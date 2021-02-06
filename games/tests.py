from django.test import TestCase
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate

from .views import *

class PlayerTest(TestCase):

    def tearDown(self):
        User.objects.all().delete()
    def test_model(self):
        user = User.objects.create()
        self.assertTrue(user.profile.player)

class GameTest(APITestCase):
    def tearDown(self):
        User.objects.all().delete()
        Game.objects.all().delete()
        Challenge.objects.all().delete()
        Reward.objects.all().delete()
        Achievement.objects.all().delete()
        Award.objects.all().delete() 
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
        self.challenge = Challenge.objects.create(
            problem=question,
            solution=answer,
            game=self.game,
        )

    def test_achievement_signal(self):
        import ipdb; ipdb.set_trace()
        self.test_challenge_model()
        Reward.objects.create(
            unique=True,
            challenge=self.challenge,    
        )
        Achievement.objects.create(
                player=self.user.profile.player,
                challenge=self.challenge,
        )





    def test_challenge_post(self):
        user = User.objects.create(is_superuser=True,is_staff=True)
        game = Game.objects.create()        
        url = reverse('challenge-list')
        self.client.force_login(user)
        data = {
            "problem": {
                "question": {
                    "text": "True",
                    "video": None,
                    "picture": None
                }
            },
            "solution": {
                "answer": {
                    "text": "True"
                }
            },
            "game": game.pk,
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code,201)


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

    def test_challenge_solved_view(self):
        self.test_challenge_model()
        self.challenge.game.players.add(self.user.profile.player)
        self.challenge.save()
        Achievement.objects.create(player=self.user.profile.player, challenge=self.challenge)
        url = reverse('challenge-solved')
        self.client.force_login(self.user)
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

    def test_challenge_solve_view(self):
        self.test_challenge_model()
        self.challenge.game.players.add(self.user.profile.player)
        self.challenge.save()
        url =reverse('challenge-solve',kwargs={'pk':self.challenge.pk})
        self.client.force_login(self.user)
        response = self.client.get(url, format='json')
        self.assertTrue(response.data['msg'])
        data = {'answer': 'True'}
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.data['msg'],'Correct')
