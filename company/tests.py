import datetime

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.test import TestCase
from rest_framework.test import APIClient
from company.models import Company


class TestCompanyAPIViewSet(TestCase):

    @classmethod
    def setUpTestData(cls):
        Company.objects.create(name='Nexflix', location='Mumbai', description='Movies')

    def setUp(self):
        self.client = APIClient()


    # def test_if_company_created_returns_201_created(self, request):
    #     data = {"name":"'Netflix'", "location":"Berlin", "description":"Movies"}
    #     response = self.client.post('/api/v1/companies/', data)
    #     self.assertEqual(response.status_code, 201)

    def test_get_company_list(self):
        response = self.client.get('/api/v1/companies/')
        self.assertEqual(response.status_code, 200)