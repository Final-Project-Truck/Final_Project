import datetime
import tempfile

from PIL import Image
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.test import TestCase
from rest_framework.test import APIClient

from baseuser.models import BaseUsers
from company.models import Company


class TestBaseUsersAPIViewSet(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.first_django_user = User.objects.create_user(
            id=100,
            username='person',
            password='name1',
            email='name1@gmail.com')

        cls.second_django_user = User.objects.create_user(
            id=101,
            username='company',
            password='name2',
            email='name2@gmail.com')

        cls.person_user = BaseUsers.objects.create(
            id=100,
            username='person',
            password='name1',
            email='name1@gmail.com',
            date_created=datetime.date.fromisocalendar,
            django_user=cls.first_django_user, user_type='per')

        cls.company_user = BaseUsers.objects.create(
            id=101,
            username='company',
            password='name2',
            email='name2@gmail.com',
            date_created=datetime.date.fromisocalendar,
            django_user=cls.second_django_user, user_type='com')

        cls.company = Company.objects.create(
            id=500,
            name='test_company',
            location='company_location',
            description='company_description')

    def setUp(self):
        self.client = APIClient()
        super().setUp()
        self.tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image = Image.new('RGB', (100, 100))
        image.save(self.tmp_file.name)
        self.params = {
            'picture': self.tmp_file
        }

    @classmethod
    def tearDownClass(cls):
        cls.company.clean()
        cls.first_django_user.clean()
        cls.second_django_user.clean()
        cls.person_user.clean()
        cls.company_user.clean()
        cls.company.clean()

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
        response = self.client.get('/api/v1/baseusers/100/')
        self.assertEqual(response.status_code, 200)

    def test_if_baseuser_is_updated_returns_200_ok(self):
        response = self.client.get('/api/v1/baseusers/100/')
        response.data['username'] = 'Divya'
        self.client.put('/api/v1/baseusers/1/', response.data)
        self.assertEqual(response.status_code, 200)

    def test_if_django_user_is_updated_when_baseuser_is_updated(self):
        response = self.client.get('/api/v1/baseusers/100/')
        response.data['password'] = 'name1' # since password is write only
        # now it is not returned in the response body
        print(response.data)
        response.data['username'] = 'Divya'
        print(response.data)
        resopnse2=self.client.put('/api/v1/baseusers/100/', response.data)
        print(resopnse2.data)
        print(resopnse2)
        django_user = User.objects.get(baseuser=100)
        print(django_user)
        self.assertEqual(django_user.username, 'Divya')

    def test_if_baseuser_is_deleted(self):
        response = self.client.get('/api/v1/baseusers/100/')
        self.client.delete('/api/v1/baseusers/100/', response.data)
        self.assertEqual(response.status_code, 200)

    def test_if_django_user_is_deleted_if_baseuser_is_deleted(self):
        response = self.client.get('/api/v1/baseusers/100/')
        self.client.delete('/api/v1/baseusers/100/', response.data)
        response = User.objects.filter(email='name1@gmail.com')
        self.assertEqual(response.exists(), False)

    """User Profile Tests"""

    def test_if_person_can_create_a_user_profile(self):
        # log in as a person user
        self.client.login(username='person',
                          password='name1')
        data = {"base_user": 100, "current_company": 500,
                "past_companies": [], "about": "text",
                'picture': (self.params['picture'])}

        response = self.client.post('/api/v1/user-profile/', data=data,
                                    format='multipart')
        self.assertIn('picture', response.data),
        self.assertEqual(response.status_code, 201),
        self.client.logout()

    def test_if_default_picture_is_assigned_to_user_profile(self):
        # log in as a person user
        self.client.login(username='person',
                          password='name1')
        data = {"base_user": 100, "current_company": 500,
                "past_companies": [],
                "about": "text"}

        response = self.client.post('/api/v1/user-profile/', data=data,
                                    format='multipart')

        self.assertEqual(response.status_code, 201),

        self.assertIn("picture", response.data)
        self.client.logout()

    """Company Profile Tests"""

    def test_if_company_can_create_a_company_profile(self):
        # retrieve a company_user
        # company_user = BaseUsers.objects.get(id=101)
        # log in as a company user
        self.client.login(username='company',
                          password='name2')  # since  the passwort is now
        # hashed
        # during saving we can not retrieve it and pass it to login
        data = {"base_user": 101, "company": 500,
                "website": "https://www.google.com/",
                "number_of_employees": 100,
                "organization_type": "pub", "revenue": 1000}
        response = self.client.post('/api/v1/company-profile/', data)
        self.assertEqual(response.status_code, 201)
        self.client.logout()
