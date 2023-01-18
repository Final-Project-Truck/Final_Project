import datetime
from django.test import TestCase
from django.test import TransactionTestCase

from django.contrib.auth.models import User
from rest_framework.test import APIClient
from baseuser.models import BaseUsers
from company.models import Company
from survey.models import Survey, Question, SurveyQuestion, Submission


class TestSurveyAPIViewSet(TestCase):
    reset_sequences = True

    @classmethod
    def setUpTestData(cls):
        cls.django_user = User.objects.create_user(
             username='name10', password='name10', email='name10@gmail.com')

        cls.django_user2 = User.objects.create_user(
            username='name11', password='name11', email='name11@gmail.com')

        cls.django_company_user = User.objects.create_user(
            username='cname', password='cname', email='cname@gmail.com')

        cls.user = BaseUsers.objects.create(
            username='name10', password1='name10', password2='name10',
            email='name10@gmail.com',
            date_created=datetime.date.fromisocalendar,
            user_type='per',
            django_user=cls.django_user)

        cls.user2 = BaseUsers.objects.create(
            username='name11', password1='name11', password2='name11',
            email='name11@gmail.com',
            date_created=datetime.date.fromisocalendar,
            user_type='per',
            django_user=cls.django_user2)

        cls.company_user = BaseUsers.objects.create(
            username='cname', password1='cname', password2='cname',
            email='cname@gmail.com',
            date_created=datetime.date.fromisocalendar,
            user_type='com',
            django_user=cls.django_company_user)

        cls.company = Company.objects.create(
            name='peter', location='here', description='text')

        cls.company2 = Company.objects.create(
            name='peter2', location='here', description='text')

        cls.template_survey = Survey.objects.create(
            title='peter', is_active=False, creator_id=None,
            company_id=cls.company.id, created_at='2022-12-12')

        cls.template_survey_2 = Survey.objects.create(
            title='peter2', is_active=False, creator_id=None,
            company_id=cls.company2.id, created_at='2022-12-12')

        cls.survey1 = Survey.objects.create(
            title='User_Survey', is_active=False, creator_id=1,
            company_id=cls.company.id, created_at='2022-12-12')

        cls.survey2 = Survey.objects.create(
            title='Active_Survey', is_active=False, creator_id=2,
            company_id=cls.company.id, created_at='2022-12-12')

        cls.template_question_1 = Question.objects.create(
            prompt="Question 1", type='txt', template_question=True)

        cls.template_question_2 = Question.objects.create(
            prompt="Question 2", type='txt', template_question=True)

        cls.template_question_3 = Question.objects.create(
            prompt="Question 3", type='txt', template_question=True)

        cls.surveyquestion1 = SurveyQuestion.objects.create(
            survey=cls.template_survey, question=cls.template_question_1)

        cls.surveyquestion2 = SurveyQuestion.objects.create(
            survey=cls.template_survey, question=cls.template_question_2)

        cls.surveyquestion3 = SurveyQuestion.objects.create(
            survey=cls.template_survey, question=cls.template_question_3)

        cls.surveyquestion_1 = SurveyQuestion.objects.create(
            survey=cls.template_survey_2, question=cls.template_question_1)

        cls.surveyquestion_2 = SurveyQuestion.objects.create(
            survey=cls.template_survey_2, question=cls.template_question_2)

        cls.surveyquestion_3 = SurveyQuestion.objects.create(
            survey=cls.template_survey_2, question=cls.template_question_3)

        # Submission.objects.create(
        #     survey_id=active_survey.id,
        #     created_at='2022-12-12',
        #     is_complete=False, submitter_id=user.id)

    def setUp(self):
        self.client = APIClient()
        self.logged_in_user = self.client.login(username='name10',
                                           password='name10')
        print(self.logged_in_user)
        #print(self.client.get('/api/v1/survey/'))
        if self.logged_in_user:
            survey = Survey.objects.all()

            print(survey[1].id)
            # test = self.client.get('/api/v1/survey/3/')
            # print((self.client.get('/api/v1/survey/')).data)
            # self.assertEqual(test.status_code, 200)
            # test.data['is_active'] = True
            # self.client.put('/api/v1/survey/3/', test.data)

    # def tearDown(self):
    #     self.client.logout()
    #
    # @classmethod
    # def tearDownClass(cls):
    #     survey_in_test = Survey.objects.all()
    #     print(survey_in_test)
    #     cls.django_user.clean()
    #     cls.django_user2.clean()
    #     cls.user.clean()
    #     cls.user2.clean()
    #     cls.company.clean()
    #     cls.template_survey.clean()
    #     cls.survey1.clean()
    #     cls.survey2.clean()
    #     cls.template_question_1.clean()
    #     cls.template_question_2.clean()
    #     cls.template_question_3.clean()
    #     cls.surveyquestion1.clean()
    #     cls.surveyquestion2.clean()
    #     cls.surveyquestion3.clean()
    #     cls.surveyquestion_1.clean()
    #     cls.surveyquestion_2.clean()
    #     cls.surveyquestion_3.clean()
    #
    #
    def test_if_user_is_logged_in(self):
        self.tearDown()
        response = self.client.get('/api/v1/survey/')
        self.assertEqual(
            response.data['detail'],
            "Authentication credentials were not provided.")
    # def test_if_survey_created_returns_201_created(self):
    #     self.tearDown()
    #     self.logged_in_user = self.client.login(username='name11',
    #                      password='name11')
    #     new_survey = {"title": "'new_survey'", "is_active": False,
    #                   "creator": 2, "company": 2, "created_at":
    #                       "2022-12-12"}
    #     response = self.client.post('/api/v1/survey/', new_survey)
    #     self.assertEqual(response.status_code, 201)

    # def test_if_mult_surveys_created_for_same_com_returns_error_message(self):
    #     self.tearDown()
    #     self.logged_in_user = self.client.login(username='name11',
    #                      password='name11')
    #     new_survey = {"title": "'newest_survey'", "is_active": False,
    #                   "creator": 2, "company": 1, "created_at":
    #                       "2022-12-12"}
    #     response = self.client.post('/api/v1/survey/', new_survey)
    #     self.assertEqual(response.data,
    #                      'You cannot create multiple surveys for a company')
    #
    # def test_if_company_user_survey_created_returns_error_message(self):
    #     self.tearDown()
    #     self.logged_in_user = self.client.login(username='cname',
    #                       password='cname')
    #     new_survey = {"title": "'com_survey'", "is_active": False,
    #                   "creator": 3, "company": 2, "created_at":
    #                       "2022-12-12"}
    #     response = self.client.post('/api/v1/survey/', new_survey)
    #     self.assertEqual(response.data, 'User of type company create a '
    #                                     'survey')
    #
    #
    # def test_if_survey_created_is_active_True_returns_response_message(self):
    #     new_survey = {"title": "'Survey 2'", "is_active": True,
    #                   "creator": 1, "company": 2, "created_at":
    #                       "2022-12-12"}
    #     self.tearDown()
    #     self.logged_in_user = self.client.login(username='name11',
    #                                             password='name11')
    #     response = self.client.post('/api/v1/survey/', new_survey)
    #     self.assertEqual(response.data,
    #                      'Survey cannot be activated during creation')
    #
    # def test_survey_template_questions_added_to_survey_when_user_creates_survey(
    #         self):
    #     new_survey = {"title": "'Survey 2'", "is_active": False,
    #                   "creator": 2, "company": 2, "created_at":
    #                       "2022-12-12"}
    #     response = self.client.post('/api/v1/survey/', new_survey)
    #     print(response.data)
    #     template_questions = self.client.get('/api/v1/survey_questions/')
    #     count = 0
    #     for survey_questions in range(len(template_questions.data)):
    #         if template_questions.data[survey_questions]['survey'] == \
    #                 response.data['id']:
    #             count = count + 1
    #     self.assertEqual(count, 3)

    # '''
    # user is able to update the survey until submission is created
    # '''
    # def test_if_survey_returns_200_when_updated(self):
    #     response = self.client.get('/api/v1/survey/3/')
    #     #del response.data['template']
    #     response.data['title'] = 'Peter is awesome'
    #     updated_response = self.client.put('/api/v1/survey/3/', response.data)
    #     self.assertEqual(updated_response.data, 'Survey updated')
    #     #print((self.client.get('/api/v1/survey/3/')).data)
    #
    # def test_message_when_active_submission_and_user_closes_survey(self):
    #     response = self.client.get('/api/v1/survey/3/')
    #     #print(response.data)
    #     submission = {"is_complete": False, "survey": 3,
    #                   "submitter": 1, "created_at": "2022-12-12"}
    #     post = self.client.post('/api/v1/submissions/', submission)
    #     #print(post.data)
    #     response.data['is_active'] = False
    #     updated_response = self.client.put('/api/v1/survey/3/', response.data)
    #     #print(response.data)
    #     self.assertEqual(updated_response.data, 'Cannot inactivate/update '
    #                                             'survey, submission is already created.')
    #
    # def test_if_user_created_submission_returns_201(self):
    #     submission = {"is_complete": False, "survey": 3,
    #                   "submitter": 1, "created_at": "2022-12-12"}
    #     response = self.client.post('/api/v1/submissions/', submission)
    #     self.assertEqual(response.status_code, 201)
    #
    # def test_if_user_created_submission_fails_when_survey_is_inactive(self):
    #     submission = {"is_complete": False, "survey": 2,
    #                   "submitter": 1, "created_at": "2022-12-12"}
    #     response = self.client.post('/api/v1/submissions/', submission)
    #     self.assertEqual(response.data,
    #                      'Survey is not active, cannot create submission')

