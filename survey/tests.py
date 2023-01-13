import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from baseuser.models import BaseUsers
from company.models import Company
from survey.models import Survey, Question, SurveyQuestion


class TestSurveyAPIViewSet(TestCase):

    @classmethod
    def setUpTestData(cls):
        django_user = User.objects.create_user(
            username='name1', password='name1', email='name1@gmail.com')

        BaseUsers.objects.create(
            username='name1', password1='name1', password2='name1',
            email='name1@gmail.com',
            date_created=datetime.date.fromisocalendar,
            django_user=django_user)

        company = Company.objects.create(
            name='peter', location='here', description='text')

        template_survey = Survey.objects.create(
            title='Template_Survey', is_active=False, creator_id=None,
            company_id=company.id, created_at='2022-12-12',
            template_id=company.id)

        template_question_1 = Question.objects.create(
            prompt="Question 1", type='txt', template_question=True)

        template_question_2 = Question.objects.create(
            prompt="Question 2", type='txt', template_question=True)

        template_question_3 = Question.objects.create(
            prompt="Question 3", type='txt', template_question=True)

        SurveyQuestion.objects.create(
            survey=template_survey, question=template_question_1)

        SurveyQuestion.objects.create(
            survey=template_survey, question=template_question_2)

        SurveyQuestion.objects.create(
            survey=template_survey, question=template_question_3)

    def setUp(self):
        self.client = APIClient()

    def test_which_companies_are_created(self):
        response = self.client.get('/api/v1/companies/')
        print(response.data)
        self.assertEqual(response.status_code, 200)

    def test_which_ueser_are_created(self):
        response = self.client.get('/api/v1/baseusers/')
        print(response.data)
        self.assertEqual(response.status_code, 200)

    def test_which_survey_are_created(self):
        response = self.client.get('/api/v1/survey/')
        print(response.data)
        self.assertEqual(response.status_code, 200)

    def test_if_survey_created_returns_201_created(self):
        new_survey = {"title": "'Survey 2'", "is_active": False,
                      "creator": 4, "company": 4, "created_at":
                          "2022-12-12", "template": ''}
        response = self.client.post('/api/v1/survey/', new_survey)
        self.assertEqual(response.status_code, 201)
