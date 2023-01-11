import datetime
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.test import TestCase
from rest_framework.test import APIClient
from baseuser.models import BaseUsers


class TestBaseUsersAPIViewSet(TestCase):

    @classmethod
    def setUpTestData(cls):
        django_user = User.objects.create_user(username='name1',
                                               password='name1',
                                               email='name1@gmail.com')
        BaseUsers.objects.create(username='name1', password1='name1',
                                 password2='name1', email='name1@gmail.com',
                                 date_created=datetime.date.fromisocalendar,
                                 django_user=django_user)

    def setUp(self):
        self.client = APIClient()

    def test_if_baseuser_created_returns_201_created(self):
        data = {"username": "'name2'", "password": "name2",
                "email": "name2@gmail.com"}
        response = self.client.post('/api/v1/baseusers/', data)
        self.assertEqual(response.status_code, 201)

    def test_if_djangouser_is_created_returns_True_if_exists(self):
        data = {"username": "'name2'", "password": "name2",
                "email": "name2@gmail.com"}
        self.client.post('/api/v1/baseusers/', data)
        output = get_object_or_404(User, email="name2@gmail.com")
        self.assertNotEqual(output, 404)

    def test_get_baseuser_list(self):
        response = self.client.get('/api/v1/baseusers/')
        self.assertEqual(response.status_code, 200)

    def test_get_baseuser_instance_returns_200_ok(self):
        response = self.client.get('/api/v1/baseusers/1/')
        self.assertEqual(response.status_code, 200)

    def test_if_baseuser_is_updated_returns_200_ok(self):
        response = self.client.get('/api/v1/baseusers/1/')
        response.data['username'] = 'Divya'
        self.client.put('/api/v1/baseusers/1/', response.data)
        self.assertEqual(response.status_code, 200)

    def test_if_django_user_is_updated_when_baseuser_is_updated(self):
        response = self.client.get('/api/v1/baseusers/1/')
        response.data['username'] = 'Divya'
        self.client.put('/api/v1/baseusers/1/', response.data)
        django_user = User.objects.get(email=response.data['email'])
        self.assertEqual(django_user.username, 'Divya')

    def test_if_baseuser_is_deleted(self):
        response = self.client.get('/api/v1/baseusers/1/')
        self.client.delete('/api/v1/baseusers/1/', response.data)
        self.assertEqual(response.status_code, 200)

    def test_if_djangouser_is_deleted_if_baseuser_is_deleted(self):
        response = self.client.get('/api/v1/baseusers/1/')
        self.client.delete('/api/v1/baseusers/1/', response.data)
        response = User.objects.filter(email='name1@gmail.com')
        self.assertEqual(response.exists(), False)
