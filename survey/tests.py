import datetime
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.test import TestCase
from rest_framework.test import APIClient
from baseuser.models import BaseUsers
from company.models import Company
from survey.models import Survey


class TestSurveyAPIViewSet(TestCase):
    @classmethod
    def setUpTestData(cls):
        company = Company.objects.create(name='company12',
                                         location='Hannover',
                               description='it-company')
        user = User.objects.create_user(username='username1',
                                        password='password1',
                                        email='email1@email.com')

        baseuser = BaseUsers.objects.create(username=user.username,
                                        password1=user.password,
                                          password2=user.password,
                                        email=user.email, django_user=user)

        Survey.objects.create(title='title1', creator_id=baseuser.id,
                              company_id=company.id)

        Survey.objects.create(title='title2', creator_id=baseuser.id,
                              company_id=company.id)

        Survey.objects.create(title='title3', creator_id=baseuser.id,
                              company_id=company.id)

    def setUp(self):
        self.client = APIClient()

    def test_returns_expected_entries_which_exit(self):
        response = self.client.get('/api/v1/surveys/?search=title1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    # def test_returns_expected_entries(self):
    #     data = {"title": "title1", "creator": 'creator1', "company":
    #         "company1@gmail.com"}
    #     response = self.client.get('/api/v1/surveys/?search=thing')
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_if_data_ok(self):
    #     data = {"title": "title1", "creator": 'creator1', "company":
    #         "company1@gmail.com"}
    #     response = self.client.get('/api/v1/surveys/?search=thing')
    #     self.assertEqual(response.status_code, 200)
    # def test_if_survey_created_returns_201_created(self):
    #     data = {"username": "'name2'", "password": "name2",
    #             "email": "name2@gmail.com"}
    #     response = self.client.post('/api/v1/baseusers/', data)
    #     self.assertEqual(response.status_code, 201)
    #
    # def test_if_djangouser_is_created_returns_True_if_exists(self):
    #     data = {"username": "'name2'", "password": "name2",
    #             "email": "name2@gmail.com"}
    #     self.client.post('/api/v1/baseusers/', data)
    #     output = get_object_or_404(User, email="name2@gmail.com")
    #     self.assertNotEqual(output, 404)
    #
    # def test_get_baseuser_list(self):
    #     response = self.client.get('/api/v1/baseusers/')
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_get_baseuser_instance_returns_200_ok(self):
    #     response = self.client.get('/api/v1/baseusers/1/')
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_if_baseuser_is_updated_returns_200_ok(self):
    #     response = self.client.get('/api/v1/baseusers/1/')
    #     response.data['username'] = 'Divya'
    #     self.client.put('/api/v1/baseusers/1/', response.data)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_if_django_user_is_updated_when_baseuser_is_updated(self):
    #     response = self.client.get('/api/v1/baseusers/1/')
    #     response.data['username'] = 'Divya'
    #     self.client.put('/api/v1/baseusers/1/', response.data)
    #     django_user = User.objects.get(email=response.data['email'])
    #     self.assertEqual(django_user.username, 'Divya')
    #
    # def test_if_baseuser_is_deleted(self):
    #     response = self.client.get('/api/v1/baseusers/1/')
    #     self.client.delete('/api/v1/baseusers/1/', response.data)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_if_djangouser_is_deleted_if_baseuser_is_deleted(self):
    #     response = self.client.get('/api/v1/baseusers/1/')
    #     self.client.delete('/api/v1/baseusers/1/', response.data)
    #     response = User.objects.filter(email='name1@gmail.com')
    #     self.assertEqual(response.exists(), False)
