from django.test import TestCase
from django.contrib.auth.models import User
class TestProfile(TestCase):
    def test_create(self):
        import ipdb; ipdb.set_trace()
        user = User.objects.create()
        self.assertTrue(user.profile)
