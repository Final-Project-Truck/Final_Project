import datetime
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.test import TestCase
from rest_framework.test import APIClient
from baseuser.models import BaseUsers, UserProfile, CompanyProfile
from company.models import Company


class TestBaseUsersAPIViewSet(TestCase):

    @classmethod
    def setUpTestData(cls):
        first_django_user = User.objects.create_user(
            username='name1',
            password='name1',
            email='name1@gmail.com')

        second_django_user = User.objects.create_user(
            username='name2',
            password='name2',
            email='name2@gmail.com')

        person_user = BaseUsers.objects.create(
            username='person',
            password1='name1',
            password2='name1', email='name1@gmail.com',
            date_created=datetime.date.fromisocalendar,
            django_user=first_django_user, user_type='per')

        company_user = BaseUsers.objects.create(
            username='name2',
            password1='name2',
            password2='name2', email='name2@gmail.com',
            date_created=datetime.date.fromisocalendar,
            django_user=second_django_user, user_type='com')

        company = Company.objects.create(
            name='company_name',
            location='company_location',
            description='company_description')

        UserProfile.objects.create(
            base_user_id=person_user.id, current_company_id=company.id,
            picture='tinyurl.com/2a382vsm', about="text"
            )

        CompanyProfile.objects.create(
            base_user_id=company_user.id, company_id=company.id,
            website="https://www.person.com/",
            number_of_employees=100,
            organization_type='pub',
            revenue=1000
        )

    def setUp(self):
        self.client = APIClient()

    def test_if_person_baseuser_created_returns_201_created(self):
        data = {"username": "'name3'", "password": "name3",
                "email": "name3@gmail.com", "user_type": "per"}
        response = self.client.post('/api/v1/baseusers/', data)
        self.assertEqual(response.status_code, 201)

    def test_if_company_baseuser_created_returns_201_created(self):
        data = {"username": "'name3'", "password": "name3",
                "email": "name3@gmail.com", "user_type": "com"}
        response = self.client.post('/api/v1/baseusers/', data)
        self.assertEqual(response.status_code, 201)

    def test_if_djangouser_is_created_returns_True_if_exists(self):
        data = {"username": "'name3'", "password": "name3",
                "email": "name3@gmail.com", "user_type": "com"}
        self.client.post('/api/v1/baseusers/', data)
        output = get_object_or_404(User, email="name3@gmail.com")
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

    def test_if_django_user_is_deleted_if_baseuser_is_deleted(self):
        response = self.client.get('/api/v1/baseusers/1/')
        self.client.delete('/api/v1/baseusers/1/', response.data)
        response = User.objects.filter(email='name1@gmail.com')
        self.assertEqual(response.exists(), False)
