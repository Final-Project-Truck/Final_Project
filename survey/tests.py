import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from baseuser.models import BaseUsers
from company.models import Company
from survey.models import Survey, Question, SurveyQuestion, Submission


class TestSurveyAPIViewSet(TestCase):

    @classmethod
    def setUpTestData(cls):
        django_user = User.objects.create_user(
            username='name1', password='name1', email='name1@gmail.com')

        user = BaseUsers.objects.create(
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

        Survey.objects.create(
            title='User_Survey', is_active=False, creator_id=user.id,
            company_id=company.id, created_at='2022-12-12',
            template_id=None)

        Survey.objects.create(
            title='Active_Survey', is_active=False, creator_id=user.id,
            company_id=company.id, created_at='2022-12-12',
            template_id=None)

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

        # Submission.objects.create(
        #     survey_id=active_survey.id,
        #     created_at='2022-12-12',
        #     is_complete=False, submitter_id=user.id)

    def setUp(self):
        self.client = APIClient()


    def test(self):
        test = self.client.get('/api/v1/survey/3/')
        self.assertEqual(test.status_code, 200)
        print(test.data)

        test.data['is_active'] = True
        response = self.client.put('/api/v1/survey/3/', test.data)
        print(response.data)
        # self.assertEqual(response.status_code, 201)

    # def test_if_survey_created_returns_201_created(self):
    #     new_survey = {"title": "'Survey 2'", "is_active": False,
    #                   "creator": 1, "company": 1, "created_at":
    #                       "2022-12-12", "template": ''}
    #     response = self.client.post('/api/v1/survey/', new_survey)
    #     self.assertEqual(response.status_code, 201)

    # def test_if_survey_created_is_active_True_returns_response_message(self):
    #     new_survey = {"title": "'Survey 2'", "is_active": True,
    #                   "creator": 1, "company": 1, "created_at":
    #                       "2022-12-12", "template": ''}
    #     response = self.client.post('/api/v1/survey/', new_survey)
    #     self.assertEqual(response.data,
    #                      'Survey cannot be activated during creation')

    # def test_survey_template_questions_added_to_survey_when_user_creates_survey(
    #         self):
    #     new_survey = {"id": 10, "title": "'Survey 2'", "is_active": False,
    #                   "creator": 1, "company": 1, "created_at":
    #                       "2022-12-12", "template": ''}
    #     response = self.client.post('/api/v1/survey/', new_survey)
    #     template_questions = self.client.get('/api/v1/survey_questions/')
    #     count = 0
    #     for survey_questions in range(len(template_questions.data)):
    #         if template_questions.data[survey_questions]['survey'] == \
    #                 response.data['id']:
    #             count = count + 1
    #     self.assertEqual(count, 3)

    # def test_if_survey_returns_200_when_updated(self):
    #     response = self.client.get('/api/v1/survey/3/')
    #     del response.data['template']
    #     response.data['title'] = 'Peter is awesome'
    #     self.client.put('/api/v1/survey/3/', response.data)
    #     self.assertEqual(response.status_code, 200)
    #     print(response.data)

    # def test_message_when_active_submission_and_user_closes_survey(self):
    #     response = self.client.get('/api/v1/survey/3/')
    #     del response.data['template']
    #     print(response.data)
    #     submission = {"is_complete": False, "survey": 3,
    #                   "submitter": 1, "created_at": "2022-12-12"}
    #     post = self.client.post('/api/v1/submissions/', submission)
    #     print(post.data)
    #     response.data['is_active'] = False
    #     self.client.put('/api/v1/survey/3/', response.data)
    #     print(response.data)
        # self.assertEqual(response.data,
        #                  'Cannot inactivate survey, submission is '
        #                  'already created.'
        #                  )

    # def test_if_user_created_submission_returns_201(self):
    #     submission = {"is_complete": False, "survey": 3,
    #                   "submitter": 1, "created_at": "2022-12-12"}
    #     response = self.client.post('/api/v1/submissions/', submission)
    #     self.assertEqual(response.status_code, 201)

    # def test_if_user_created_submission_fails_when_survey_is_inactive(self):
    #     submission = {"is_complete": False, "survey": 2,
    #                   "submitter": 1, "created_at": "2022-12-12"}
    #     # response = self.client.get('/api/v1/survey/2/')
    #     # print(response.data)
    #     response = self.client.post('/api/v1/submissions/', submission)
    #     self.assertEqual(response.data,
    #                      'Survey is not active, cannot create submission')

