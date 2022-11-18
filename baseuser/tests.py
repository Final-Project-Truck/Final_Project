import json

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from baseuser.models import BaseUsers
# Create your tests here.

class TestBaseUsersAPIViewSet(TestCase):

    @classmethod
    def setUpTestData(cls):
        django_user = User.objects.create_user(username='name1',password='name1',email='name1@gmail.com')
        BaseUsers.objects.create(username='name1', password='name1', email='name1@gmail.com', django_user=django_user)

    def setUp(self):
        self.client = APIClient()

    def test_if_baseuser_created_returns_201_ok(self):
        data = {"username":"'name2'", "password":"name2", "email":"name1@gmail.com"}
        response = self.client.post('/api/v1/baseusers', data)
        self.assertEqual(response.status_code, 201)

    def test_get_user_list(self):
        response = self.client.get('/api/v1/baseusers/')
        self.assertEqual(response.status_code,200)

