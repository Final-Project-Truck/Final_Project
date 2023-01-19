import datetime

from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from baseuser.models import BaseUsers
from company.models import Company
from survey.models import Survey, Question, SurveyQuestion


class TestCompanyAPIViewSet(TestCase):
    #reset_sequences = True

    @classmethod
    def setUpTestData(cls):
        cls.django_user_company_test = User.objects.create_user(
            username='ctname', password='ctname', email='ctname@gmail.com')

        cls.test_user = BaseUsers.objects.create(
            username='ctname', password1='ctname', password2='ctname',
            email='ctname@gmail.com',
            date_created=datetime.date.fromisocalendar,
            user_type='per',
            django_user=cls.django_user_company_test )

        cls.company_test = Company.objects.create(
            name='company_name',
            location='company_location',
            description='company_description')

        cls.template_survey_test = Survey.objects.create(
            title='company_name', is_active=False, creator_id=None,
            company_id=cls.company_test.id, created_at='2022-12-12')

        cls.template_question_1 = Question.objects.create(
            prompt="Question 1", type='txt', template_question=True)

        cls.template_question_2 = Question.objects.create(
            prompt="Question 2", type='txt', template_question=True)

        cls.template_question_3 = Question.objects.create(
            prompt="Question 3", type='txt', template_question=True)

        cls.surveyquestion1 = SurveyQuestion.objects.create(
            survey=cls.template_survey_test, question=cls.template_question_1)

        cls.surveyquestion2 = SurveyQuestion.objects.create(
            survey=cls.template_survey_test, question=cls.template_question_2)

        cls.surveyquestion3 = SurveyQuestion.objects.create(
            survey=cls.template_survey_test, question=cls.template_question_3)

    def setUp(self):

        self.client = APIClient()
        self.logged_in_user = self.client.login(username='ctname',
                                           password='ctname')

    def tearDown(self):
        self.client.logout()
        #self.reset_sequences = True

    @classmethod
    def tearDownClass(cls):
        cls.company_test.clean()
        cls.template_survey_test.clean()
        cls.template_question_1.clean()
        cls.template_question_2.clean()
        cls.template_question_3.clean()
        cls.surveyquestion1.clean()
        cls.surveyquestion2.clean()
        cls.surveyquestion3.clean()
        cls.test_user.clean()
        cls.django_user_company_test.clean()
        survey = Survey.objects.all()
        #survey.delete()



    def test_if_company_created_returns_201_created(self):
        data = {"name": "'company_name_1'", "location": "company_location",
                "description": "company_description"}
        response = self.client.post('/api/v1/companies/', data)
        self.assertEqual(response.status_code, 201)


    def test_if_survey_is_created_when_company_created_returns_True_if_exists(
            self):
        data = {"name": "'company_name_2'", "location": "company_location",
                "description": "company_description"}
        self.client.post('/api/v1/companies/', data)
        output = get_object_or_404(Survey, title="'company_name_2'")
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

    # def test_if_company_is_deleted(self):
    #     response = self.client.get('/api/v1/companies/1/')
    #     self.client.delete('/api/v1/companies/1/', response.data)
    #     self.assertEqual(response.status_code, 200)
