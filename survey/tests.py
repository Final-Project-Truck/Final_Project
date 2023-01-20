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
        cls.django_user = User.objects.create_user(
            id=1, username='name10',
            password='name10', email='name10@gmail.com')

        cls.django_user2 = User.objects.create_user(
            id=2, username='name11',
            password='name11', email='name11@gmail.com')

        cls.django_company_user = User.objects.create_user(
            id=3, username='cname', password='cname', email='cname@gmail.com')

        cls.django_admin = User.objects.create_user(
             id=10, username='admin',
             password='12345', email='admin@gmail.com',
             is_staff=True)

        cls.user = BaseUsers.objects.create(
            id=1, username='name10', password1='name10', password2='name10',
            email='name10@gmail.com',
            date_created=datetime.date.fromisocalendar,
            user_type='per',
            django_user=cls.django_user)

        cls.user2 = BaseUsers.objects.create(
            id=2, username='name11', password1='name11', password2='name11',
            email='name11@gmail.com',
            date_created=datetime.date.fromisocalendar,
            user_type='per',
            django_user=cls.django_user2)

        cls.company_user = BaseUsers.objects.create(
            id=3, username='cname', password1='cname', password2='cname',
            email='cname@gmail.com',
            date_created=datetime.date.fromisocalendar,
            user_type='com',
            django_user=cls.django_company_user)

        cls.admin = BaseUsers.objects.create(
            id=10, username='admin', password1='12345', password2='12345',
            email='admin@gmail.com',
            date_created=datetime.date.fromisocalendar,
            user_type='per',
            django_user=cls.django_admin)

        cls.company = Company.objects.create(
            id=501, name='peter', location='here', description='text')

        cls.company2 = Company.objects.create(
            id=502, name='peter2', location='here', description='text')

        cls.template_survey = Survey.objects.create(
            id=200, title='peter', is_active=False, creator_id=None,
            company_id=cls.company.id, created_at='2022-12-12')

        cls.template_survey_2 = Survey.objects.create(
            id=201, title='peter2', is_active=False, creator_id=None,
            company_id=cls.company2.id, created_at='2022-12-12')

        cls.survey1 = Survey.objects.create(
            id=300, title='User_Survey', is_active=False, creator_id=1,
            company_id=cls.company.id, created_at='2022-12-12')

        cls.survey2 = Survey.objects.create(
            id=301, title='Active_Survey', is_active=False, creator_id=2,
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

    def setUp(self):
        self.client = APIClient()
        self.logged_in_user = self.client.login(username='name10',
                                                password='name10')
        test = self.client.get('/api/v1/survey/300/')
        self.assertEqual(test.status_code, 200)
        test.data['is_active'] = True
        self.client.put('/api/v1/survey/300/', test.data)

    def tearDown(self):
        self.client.logout()

    @classmethod
    def tearDownClass(cls):
        cls.django_user.clean()
        cls.django_user2.clean()
        cls.user.clean()
        cls.user2.clean()
        cls.company.clean()
        cls.template_survey.clean()
        cls.survey1.clean()
        cls.survey2.clean()
        cls.template_question_1.clean()
        cls.template_question_2.clean()
        cls.template_question_3.clean()
        cls.surveyquestion1.clean()
        cls.surveyquestion2.clean()
        cls.surveyquestion3.clean()
        cls.surveyquestion_1.clean()
        cls.surveyquestion_2.clean()
        cls.surveyquestion_3.clean()

    """Authentication credentials were not provided."""
    def test_if_user_is_logged_in(self):
        self.tearDown()
        response = self.client.get('/api/v1/survey/')
        self.assertEqual(
            response.data['detail'].code, 'not_authenticated')

    """Survey Tests"""
    def test_if_survey_created_returns_201_created(self):
        self.tearDown()
        self.logged_in_user = self.client.login(username='name11',
                                                password='name11')
        new_survey = {"title": "'new_survey'", "is_active": False,
                      "creator": 2, "company": 502, "created_at":
                          "2022-12-12"}
        response = self.client.post('/api/v1/survey/', new_survey)
        self.assertEqual(response.status_code, 201)

    def test_if_mult_surveys_created_for_same_com_returns_error_message(self):
        self.tearDown()
        self.logged_in_user = self.client.login(username='name11',
                                                password='name11')
        new_survey = {"title": "'newest_survey'", "is_active": False,
                      "creator": 2, "company": 501, "created_at":
                          "2022-12-12"}
        response = self.client.post('/api/v1/survey/', new_survey)
        self.assertEqual(response.data,
                         'You cannot create multiple surveys for a company')

    def test_if_company_user_survey_created_returns_error_message(self):
        self.tearDown()
        self.logged_in_user = self.client.login(username='cname',
                                                password='cname')
        new_survey = {"title": "'com_survey'", "is_active": False,
                      "creator": 3, "company": 502, "created_at":
                          "2022-12-12"}
        response = self.client.post('/api/v1/survey/', new_survey)
        self.assertEqual(response.data,
                         'User of type company can not create a survey')

    def test_if_survey_created_is_active_True_returns_response_message(self):
        new_survey = {"title": "'Survey 2'", "is_active": True,
                      "creator": 1, "company": 502, "created_at":
                          "2022-12-12"}
        self.tearDown()
        self.logged_in_user = self.client.login(username='name11',
                                                password='name11')
        response = self.client.post('/api/v1/survey/', new_survey)
        self.assertEqual(response.data,
                         'Survey cannot be activated during creation')

    def test_survey_temp_quests_add_to_survey_when_user_creates_survey(self):
        new_survey = {"title": "'Survey 2'", "is_active": False,
                      "creator": 2, "company": 502, "created_at":
                          "2022-12-12"}
        response = self.client.post('/api/v1/survey/', new_survey)
        template_questions = self.client.get('/api/v1/survey_questions/')
        count = 0
        for survey_questions in range(len(template_questions.data)):
            if template_questions.data[survey_questions]['survey'] == \
                    response.data['id']:
                count = count + 1
        self.assertEqual(count, 3)

    '''
    user is able to update the survey until submission is created
    '''
    def test_if_survey_returns_200_when_updated(self):
        response = self.client.get('/api/v1/survey/300/')
        response.data['title'] = 'Peter is awesome'
        updated_response = self.client.put('/api/v1/survey/300/',
                                           response.data)
        self.assertEqual(updated_response.data, 'Survey updated')

    def test_message_when_active_submission_and_user_closes_survey(self):
        submission = {"is_complete": False, "survey": 300,
                      "submitter": 1, "created_at": "2022-12-12"}
        self.client.post('/api/v1/submissions/', submission)
        response = self.client.get('/api/v1/survey/300/')
        response.data['is_active'] = False
        updated_response = self.client.put('/api/v1/survey/300/',
                                           response.data)
        self.assertEqual(updated_response.data, 'Cannot inactivate/update '
                                                'survey, submission '
                                                'is already created.')

    def test_if_survey_is_deleted_when_user_deletes_survey(self):
        self.tearDown()
        self.logged_in_user = self.client.login(username='name11',
                                                password='name11')
        response = self.client.get('/api/v1/survey/301/')
        message = self.client.delete('/api/v1/survey/301/', response.data)
        self.assertEqual(message.status_code, 204)

    def test_if_survey_is_deleted_when_bad_user_deletes_inactive_survey(self):
        response = self.client.get('/api/v1/survey/301/')
        self.client.delete('/api/v1/survey/301/', response.data)
        response = Survey.objects.filter(id=301)
        self.assertEqual(response.exists(), True)

    def test_if_survey_is_deleted_when_survey_is_active(self):
        response = self.client.get('/api/v1/survey/300/')
        message = self.client.delete('/api/v1/survey/300/', response.data)
        self.assertEqual(message.data, 'Survey cannot be deleted while active')
        response = Survey.objects.filter(id=300)
        self.assertEqual(response.exists(), True)

    # def test_if_django_admin_can_delete_active_survey(self):
    #     self.tearDown()
    #     self.logged_in_user = self.client.login(username='admin',
    #                                             password='12345')
    #     response = self.client.get('/api/v1/survey/300/')
    #     self.assertEqual(response.status_code, 200)
        # message = self.client.delete('/api/v1/survey/4/', response.data)
        # self.assertEqual(message.status_code, 204)
        # response = Survey.objects.filter(id=4)
        # self.assertEqual(response.exists(), False)

    """Question Tests"""
    def test_if_user_created_choice_question_is_created(self):
        question = {"prompt": "This is a choice question", "type": "cho",
                    "template_question": False}
        response = self.client.post('/api/v1/questions/', question)
        self.assertEqual(response.status_code, 201)

    def test_if_user_created_text_question_is_created(self):
        question = {"prompt": "This is a choice question", "type": "txt",
                    "template_question": False}
        response = self.client.post('/api/v1/questions/', question)
        self.assertEqual(response.status_code, 201)

    """Submission Tests"""
    def test_if_user_created_submission_returns_201(self):
        submission = {"is_complete": False, "survey": 300,
                      "submitter": 1, "created_at": "2022-12-12"}
        response = self.client.post('/api/v1/submissions/', submission)
        self.assertEqual(response.status_code, 201)

    def test_if_user_created_submission_fails_when_survey_is_inactive(self):
        self.tearDown()
        self.logged_in_user = self.client.login(username='name11',
                                                password='name11')
        response = self.client.get('/api/v1/survey/301/')
        submission = {"is_complete": False, "survey": 301,
                      "submitter": 2, "created_at": "2022-12-12"}
        response = self.client.post('/api/v1/submissions/', submission)
        self.assertEqual(response.data,
                         'Survey is not active, cannot create submission')

    def test_if_sub_created_for_other_users_survey_returns_error_message(
            self):
        self.tearDown()
        self.logged_in_user = self.client.login(username='name11',
                                                password='name11')
        submission = {"is_complete": False, "survey": 300,
                      "submitter": 2, "created_at": "2022-12-12"}
        response = self.client.post('/api/v1/submissions/', submission)
        self.assertEqual(response.data,
                         'Submission cannot be created for other users survey')
