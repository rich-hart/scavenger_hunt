from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate

class TestProfile(APITestCase):
    def setUp(self):
        self.url = reverse('profile-list')
        self.user = User.objects.create_user(
            username='test_user',
            email='u@d.com',
            password='password',
        )
    def test_signal(self):
        self.assertTrue(self.user.profile)

    def test_anonymous_view(self):
        response = self.client.get(self.url, format='json')
        self.assertFalse(response.data)

    def test_view(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url, format='json')
        self.assertTrue(response.data)

