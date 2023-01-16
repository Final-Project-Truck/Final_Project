from django.shortcuts import get_object_or_404
from django.test import TestCase
from rest_framework.test import APIClient
from company.models import Company, JobPosting
from survey.models import Survey


class TestCompanyAPIViewSet(TestCase):

    @classmethod
    def setUpTestData(cls):
        company = Company.objects.create(name='company_name',
                                         location='company_location',
                                         description='company_description')
        JobPosting.objects.create(job_title='title',
                                  company_id=company.id,
                                  description='Job_description',
                                  salary='job_salary')

    def setUp(self):
        self.client = APIClient()

    def test_if_company_created_returns_201_created(self):
        data = {"name": "'company_name'", "location": "company_location",
                "description": "company_description"}
        response = self.client.post('/api/v1/companies/', data)
        self.assertEqual(response.status_code, 201)

    def test_if_survey_is_created_when_company_created_returns_True_if_exists(
            self):
        data = {"name": "'company_name'", "location": "company_location",
                "description": "company_description"}
        self.client.post('/api/v1/companies/', data)
        output = get_object_or_404(Survey, title="'company_name'")
        self.assertNotEqual(output, 404)

    def test_get_company_list(self):
        response = self.client.get('/api/v1/companies/')
        self.assertEqual(response.status_code, 200)

    def test_get_company_instance_returns_200_ok(self):
        response = self.client.get('/api/v1/companies/1/')
        self.assertEqual(response.status_code, 200)

    def test_if_company_is_updated_returns_200_ok(self):
        response = self.client.get('/api/v1/companies/1/')
        response.data['name'] = 'Mathiass'
        self.client.put('/api/v1/companies/1/', response.data)
        self.assertEqual(response.status_code, 200)

    def test_if_company_is_deleted(self):
        response = self.client.get('/api/v1/companies/1/')
        self.client.delete('/api/v1/companies/1/', response.data)
        self.assertEqual(response.status_code, 200)

    def test_if_jobposting_created_returns_201_created(self):
        new_data = {"job_title": "title1", "company": 1,
                    "description": "job_description1", "salary": "job_salary1"}
        response = self.client.post('/api/v1/jobposting/', new_data)
        self.assertEqual(response.status_code, 201)

    def test_get_jobposting_list(self):
        response = self.client.get('/api/v1/jobposting/')
        self.assertEqual(response.status_code, 200)

    def test_get_jobposting_instance_returns_200_ok(self):
        response = self.client.get('/api/v1/jobposting/1/')
        self.assertEqual(response.status_code, 200)

    def test_if_jobposting_is_updated_returns_200_ok(self):
        response = self.client.get('/api/v1/jobposting/1/')
        response.data['name'] = 'Mathiass'
        self.client.put('/api/v1/jobposting/1/', response.data)
        self.assertEqual(response.status_code, 200)

    def test_if_jobposting_is_deleted(self):
        response = self.client.get('/api/v1/jobposting/1/')
        self.client.delete('/api/v1/jobposting/1/', response.data)
        self.assertEqual(response.status_code, 200)

    def test_jobfiltering(self):
        pass  # todo write test cases for the filters
