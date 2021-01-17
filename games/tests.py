from django.test import TestCase
from users.models import Profile, User
class Player(TestCase):
    def test_model(self):
        user = User.objects.create()
        self.assertTrue(user.profile.player) 
