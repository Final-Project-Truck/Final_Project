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
            id=200, title='Template Survey', is_active=False, creator_id=None,
            company_id=cls.company.id, created_at='2022-12-12')

        cls.template_survey_2 = Survey.objects.create(
            id=201, title='Template Survey', is_active=False, creator_id=None,
            company_id=cls.company2.id, created_at='2022-12-12')

        cls.survey1 = Survey.objects.create(
            id=300, title='User_Survey', is_active=False, creator_id=1,
            company_id=cls.company.id, created_at='2022-12-12')

        cls.survey2 = Survey.objects.create(
            id=301, title='Active_Survey', is_active=False, creator_id=2,
            company_id=cls.company.id, created_at='2022-12-12')

        cls.template_question_1 = Question.objects.create(
            id=601, prompt="Question 1", type='txt', template_question=True)

        cls.template_question_2 = Question.objects.create(
            id=602, prompt="Question 2", type='txt', template_question=True)

        cls.template_question_3 = Question.objects.create(
            id=603, prompt="Question 3", type='txt', template_question=True)

        cls.user_question_1 = Question.objects.create(
            id=604, prompt="Are you satisfied?", type='txt',
            template_question=False)

        cls.user_question_2 = Question.objects.create(
            id=605, prompt="Are you satisfied?", type='txt',
            template_question=False)

        cls.user_survey_question = SurveyQuestion.objects.create(
            id=900, survey=cls.survey1, question=cls.user_question_2)

        cls.surveyquestion1 = SurveyQuestion.objects.create(
            id=701, survey=cls.template_survey,
            question=cls.template_question_1)

        cls.surveyquestion2 = SurveyQuestion.objects.create(
            id=702, survey=cls.template_survey,
            question=cls.template_question_2)

        cls.surveyquestion3 = SurveyQuestion.objects.create(
            id=703, survey=cls.template_survey,
            question=cls.template_question_3)

        cls.surveyquestion_1 = SurveyQuestion.objects.create(
            id=704, survey=cls.template_survey_2,
            question=cls.template_question_1)

        cls.surveyquestion_2 = SurveyQuestion.objects.create(
            id=705, survey=cls.template_survey_2,
            question=cls.template_question_2)

        cls.surveyquestion_3 = SurveyQuestion.objects.create(
            id=706, survey=cls.template_survey_2,
            question=cls.template_question_3)

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

    def test_if_question_can_be_added_after_survey_is_active(self):
        response = self.client.get('/api/v1/survey/300/')
        new_qsn = {'survey': 300, 'question': 604}
        response = self.client.post('/api/v1/survey_questions/', new_qsn)
        self.assertEqual(response.data,
                         'Survey is active, cannot add questions')

    def test_if_question_can_be_added_if_survey_is_inactive(self):
        self.tearDown()
        self.logged_in_user = self.client.login(username='name11',
                                                password='name11')
        response = self.client.get('/api/v1/survey/301/')
        new_qsn = {'survey': 301, 'question': 604}
        response = self.client.post('/api/v1/survey_questions/', new_qsn)
        self.assertEqual(response.status_code, 201)

    def test_if_duplicate_question_can_be_added_if_survey_is_inactive(self):
        self.tearDown()
        self.logged_in_user = self.client.login(username='name11',
                                                password='name11')
        new_qsn = {'survey': 301, 'question': 604}
        self.client.post('/api/v1/survey_questions/', new_qsn)
        duplicate_post = self.client.post('/api/v1/survey_questions/', new_qsn)
        self.assertEqual(duplicate_post.data,
                         'Chosen Question is already added to the survey')

    def test_if_user_can_update_survey_that_is_not_chosen(self):
        self.tearDown()
        self.logged_in_user = self.client.login(username='name11',
                                                password='name11')
        new_qsn = {'id': 15, 'survey': 301, 'question': 604}
        self.client.post('/api/v1/survey_questions/', new_qsn)
        survey_qsn = self.client.get('/api/v1/survey_questions/15/')
        survey_qsn.data['survey'] = 300
        update_post = self.client.put(
            '/api/v1/survey_questions/15/', survey_qsn.data)
        self.assertEqual(
            update_post.data, 'Edit only questions for chosen survey')

    def test_if_template_survey_qsn_can_be_deleted_from_survey(self):
        response = self.client.delete('/api/v1/survey_questions/701/')
        self.assertEqual(
            response.data['detail'],
            'You do not have permission to perform this action.')
    # def test_if_survey_qsn_can_be_deleted_when_survey_is_active(self):
    #     response_1 = self.client.get('/api/v1/survey/300/')
    #     response_1.data['is_active']=False
    #     self.client.post('/api/v1/survey/300/', response_1.data)
    #     #new_qsn = {'survey': 301, 'question': 604}
    #     response_2 = self.client.post(
    #         '/api/v1/survey_questions/', self.user_question_1)
    #     print(response_2.data)
    #     response_1.data['is_active']=True
    #     self.client.post('/api/v1/survey/300/', response_1.data)
    #     #self.client.delete()
    #     #self.assertEqual(response.status_code, 201)

    def test_if_survey_can_be_updated_after_submission_creation(self):
        submission = {"is_complete": False, "survey": 300,
                      "submitter": 1, "created_at": "2022-12-12"}
        self.client.post('/api/v1/submissions/', submission)
        response = self.client.get('/api/v1/survey/300/')
        response.data['title'] = 'Awesome'
        updated_response = self.client.put('/api/v1/survey/300/',
                                           response.data)
        self.assertEqual(updated_response.data,
                         'Cannot update the survey,'
                         'submission is already created.')

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

    def test_if_template_survey_can_be_edited(self):
        response = self.client.get('/api/v1/survey/200/')
        response.data['title'] = 'Template survey'
        updated_response = self.client.put('/api/v1/survey/200/',
                                           response.data)
        self.assertEqual(updated_response.data['detail'],
                         'You do not have permission to perform this action.')

    """Admin tests"""
    def test_if_admin_can_create_survey(self):
        self.tearDown()
        self.logged_in_user = self.client.login(username='admin',
                                                password='12345')
        new_survey = {"title": "'Survey 2'", "is_active": False,
                      "creator": 10, "company": 502, "created_at":
                          "2022-12-12"}
        response = self.client.post('/api/v1/survey/', new_survey)
        self.assertEqual(response.data, 'Admin cannot create a survey')

    def test_if_django_admin_can_delete_active_survey(self):
        self.tearDown()
        self.logged_in_user = self.client.login(username='admin',
                                                password='12345')
        response = self.client.get('/api/v1/survey/300/')
        self.assertEqual(response.status_code, 200)
        message = self.client.delete('/api/v1/survey/300/', response.data)
        self.assertEqual(message.status_code, 204)
        response = Survey.objects.filter(id=300)
        self.assertEqual(response.exists(), False)

    def test_if_admin_can_update_survey(self):
        self.tearDown()
        self.logged_in_user = self.client.login(username='admin',
                                                password='12345')
        response = self.client.get('/api/v1/survey/300/')
        response.data['is_active'] = False
        updated_response = self.client.put('/api/v1/survey/300/',
                                           response.data)
        self.assertEqual(updated_response.data, 'Admin cannot update a survey')

    def test_if_admin_can_delete_template_survey(self):
        self.tearDown()
        self.logged_in_user = self.client.login(username='admin',
                                                password='12345')
        self.client.get('/api/v1/survey/200/')
        delete_response = self.client.delete('/api/v1/survey/200/')
        self.assertEqual(delete_response.data,
                         'Template Survey cannot be deleted')

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

    # def test_if_user_creates_submission_with_is_complete_returns_error(self):
    #     submission = {"is_complete": True, "survey": 300,
    #                   "submitter": 1, "created_at": "2022-12-12"}
    #     response = self.client.post('/api/v1/submissions/', submission)
    #     self.assertEqual(response.status_code,
    #                      'Submission cannot be completed during creation, '
    #                         'Please uncheck is_complete')

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

    def test_if_sub_created_for_template_survey_returns_error_message(
            self):
        self.tearDown()
        self.logged_in_user = self.client.login(username='name11',
                                                password='name11')
        submission = {"is_complete": False, "survey": 200,
                      "submitter": 2, "created_at": "2022-12-12"}
        response = self.client.post('/api/v1/submissions/', submission)
        self.assertEqual(response.data,
                         'Submission cannot be created for template survey')
