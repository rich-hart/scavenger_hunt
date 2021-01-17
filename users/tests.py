from django.test import TestCase
from django.contrib.auth.models import User
class TestProfile(TestCase):
    def test_create(self):
        user = User.objects.create()
        self.assertTrue(user.profile)
