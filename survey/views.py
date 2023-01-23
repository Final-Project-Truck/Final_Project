# import matplotlib
# import matplotlib.pyplot as plt
# import numpy as np

from django.db import transaction
from rest_framework import status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from authentication.permissions import IsOwner, IsSurveyOwner, \
    IsSubmissionOwner
from company.models import Company
from survey.models import Survey, Question, Option, Submission, AnswerChoice, \
    AnswerText, SurveyQuestion
from survey.serializers import SurveySerializer, QuestionSerializer, \
    OptionSerializer, SubmissionSerializer, \
    AnswerChoiceSerializer, AnswerTextSerializer, SurveyQuestionSerializer


class SurveyAPIViewSet(ModelViewSet):
    search_fields = ['title', 'company__name',]
    filter_backends = (filters.SearchFilter,)
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [IsAuthenticated, IsOwner]

    # def get_queryset(self):
    #     return self.queryset.filter(creator=self.request.user.id )
    '''
    Create a survey. Set is_active to False.
    Survey can be activated only if the questions are added to it.
    '''

    def create(self, request, *args, **kwargs):
        serializer = SurveySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        title = serializer.data['title']
        # created_at = serializer.data['created_at']
        company = serializer.data['company']
        is_active = serializer.data['is_active']

        if request.user.is_staff:
            return Response('Admin cannot create a survey')
        elif request.user.baseuser.user_type == 'per':
            ''' Check if the user already created a survey for the company'''
            if Survey.objects.filter(creator_id=request.user.baseuser.id,
                                     company_id=company):
                return Response('You cannot create '
                                'multiple surveys for a company')
            else:
                with transaction.atomic():
                    if serializer.data['is_active']:
                        return Response(
                            'Survey cannot be activated during creation')
                    else:
                        new_survey = Survey.objects.create(
                            title=title,
                            # created_at=created_at,
                            company_id=company,
                            creator_id=request.user.baseuser.id,
                            is_active=is_active)
                        new_survey.save()
                        """Get Company's template survey"""
                        Company.objects.get(
                            id=new_survey.company_id)
                        template_survey = Survey.objects.get(
                            company_id=company, creator_id=None)
                        """Get the Questions related to the template survey"""
                        template_questions = SurveyQuestion.objects.filter(
                            survey_id=template_survey.id)
                        question_ids = []
                        for template_question in template_questions:
                            question_ids.append(template_question.question_id)
                        template_question_1 = Question.objects.get(
                            id=question_ids[0])
                        template_question_2 = Question.objects.get(
                            id=question_ids[1])
                        template_question_3 = Question.objects.get(
                            id=question_ids[2])

                        """insert template survey questions
                         into new created survey"""
                        survey_question_1 = SurveyQuestion.objects.create(
                            survey=new_survey, question=template_question_1)
                        survey_question_1.save()
                        survey_question_2 = SurveyQuestion.objects.create(
                            survey=new_survey, question=template_question_2)
                        survey_question_2.save()
                        survey_question_3 = SurveyQuestion.objects.create(
                            survey=new_survey, question=template_question_3)
                        survey_question_3.save()

                        # self.generate_report()
                    return Response(SurveySerializer(new_survey).data,
                                    status=201)
        else:
            return Response('User of type company can not create a survey')

    # def generate_report(self):
    #     matplotlib.use('Agg')
    #     template_questions = Question.objects.filter(
    #         template_question=True)
    #     q1 = str(template_questions[0])
    #     q2 = str(template_questions[1])
    #     q3 = str(template_questions[2])
    #     x = np.array([q1, q2, q3])
    #     y = np.array([35, 25, 25])
    #
    #     plt.plot(x, y)
    #     plt.savefig('chart2.png')
    #
    #     return 1

    '''
    Do not allow user to inactivate the survey if submission is created for it
    '''
    def update(self, request, *args, **kwargs):
        survey = self.get_object()
        serializer = self.get_serializer(survey, data=request.data)
        serializer.is_valid(raise_exception=True)

        survey_submission = Submission.objects.filter(survey_id=survey.id)

        if request.user.is_staff:
            return Response('Admin cannot update a survey')
        elif survey_submission and not serializer.validated_data['is_active']:
            return Response('Cannot inactivate/update survey, submission is '
                            'already created.')
        elif survey_submission:
            return Response('Cannot update the survey,submission is already '
                            'created.')
        else:
            Survey.objects.filter(
                id=survey.id).update(
                title=serializer.validated_data['title'],
                # created_at=serializer.validated_data['created_at'],
                company=serializer.validated_data['company'],
                is_active=serializer.validated_data['is_active'])
            return Response('Survey updated', status=201)

    def destroy(self, request, *args, **kwargs):
        survey_chosen = self.get_object()
        if request.user.is_staff:
            if survey_chosen.creator is None:
                return Response('Template Survey cannot be deleted')
            else:
                self.perform_destroy(survey_chosen)
                return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.user.baseuser and not survey_chosen.is_active:
            self.perform_destroy(survey_chosen)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('Survey cannot be deleted while active')

    def perform_destroy(self, survey_chosen):
        with transaction.atomic():
            survey_chosen.delete()


class QuestionAPIViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        question = self.get_object()
        serializer = self.get_serializer(question, data=request.data)
        serializer.is_valid(raise_exception=True)

        survey_question = SurveyQuestion.objects.filter(
            question_id=question.id)
        with transaction.atomic():
            if question.template_question:
                return Response('Cannot update template questions')
            elif survey_question:
                return Response('Question is used in another survey and '
                                'cannot edit it')
            else:
                Question.objects.filter(id=question.id).update(
                    prompt=serializer.validated_data['prompt'],
                    type=serializer.validated_data['type'],
                    template_question='f')
                return Response('Question updated')

    def destroy(self, request, *args, **kwargs):
        question = self.get_object()
        survey_question = SurveyQuestion.objects.filter(
            question_id=question.id)
        with transaction.atomic():
            if question.template_question:
                return Response('Cannot delete template questions')
            elif survey_question:
                return Response('Question is used in another survey and '
                                'cannot delete it')
            else:
                self.perform_destroy(question)
                return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, question):
        with transaction.atomic():
            question.delete()


class SurveyQuestionAPIViewSet(ModelViewSet):
    queryset = SurveyQuestion.objects.all()
    serializer_class = SurveyQuestionSerializer
    permission_classes = [IsAuthenticated, IsSurveyOwner]

    '''
    Add questions to the survey, if the survey is not active.
    Activate it, if the survey is ready to be answered.
    '''

    def create(self, request, *args, **kwargs):
        serializer = SurveyQuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        survey = serializer.data['survey']
        question = serializer.data['question']

        survey_chosen = Survey.objects.get(id=survey)

        if survey_chosen.is_active:
            return Response('Survey is active, cannot add questions')
        else:
            survey_question = SurveyQuestion.objects.filter(
                survey_id=survey,
                question_id=question)
            if not survey_question:
                SurveyQuestion.objects.create(survey_id=survey,
                                              question_id=question)
                return Response(serializer.data, status=201)
            else:
                return Response(
                    'Chosen Question is already added to the survey')

    '''
    Update the questions in the survey, if the survey is not active.
    '''

    def update(self, request, *args, **kwargs):
        survey_question = self.get_object()
        serializer = self.get_serializer(survey_question, data=request.data)
        serializer.is_valid(raise_exception=True)

        survey_chosen = Survey.objects.get(id=survey_question.survey_id,
                                           creator=request.user.id)

        if survey_chosen.is_active:
            return Response('Survey is active, cannot update questions')
        else:
            if serializer.validated_data['survey'].id is not \
                    survey_question.survey_id:
                return Response('Edit only questions for chosen survey')
            elif serializer.data['survey'] == survey_question.survey_id:
                SurveyQuestion.objects.filter(id=survey_question.id,
                                              survey_id=survey_chosen.id).\
                    update(question=serializer.validated_data['question'])
                return Response('Survey_Question updated', status=201)

    def destroy(self, request, *args, **kwargs):
        survey_question = self.get_object()
        survey_chosen = Survey.objects.get(
            id=survey_question.survey_id)
        question_chosen = Question.objects.get(id=survey_question.question_id)
        with transaction.atomic():
            if survey_chosen.is_active:
                return Response('Cannot delete survey when active')
            elif question_chosen.template_question:
                return Response(
                    'You do not have permission to perform this action.')
            else:
                self.perform_destroy(survey_question)
                return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, survey_question):
        with transaction.atomic():
            survey_question.delete()


class OptionAPIViewSet(ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        option = self.get_object()
        serializer = self.get_serializer(option, data=request.data)
        serializer.is_valid(raise_exception=True)

        survey_question = SurveyQuestion.objects.filter(
            question_id=option.question_id)

        question = Question.objects.get(id=option.question_id)
        with transaction.atomic():
            if question.template_question:
                return Response('Cannot update template options')
            elif survey_question:
                return Response('Option is used in another survey and '
                                'cannot edit it')
            else:
                Option.objects.filter(id=option.id).update(
                    text=serializer.validated_data['text'],
                    question_id=serializer.validated_data['question'])
                return Response('Options updated')

    def destroy(self, request, *args, **kwargs):
        option = self.get_object()
        survey_option = SurveyQuestion.objects.filter(
            question_id=option.question.id)
        with transaction.atomic():
            if option.template_question:
                return Response('Cannot delete template options')
            elif survey_option:
                return Response('Option is used in another survey and '
                                'cannot delete it')
            else:
                self.perform_destroy(option)
                return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, option):
        with transaction.atomic():
            option.delete()


class SubmissionAPIViewSet(ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated, IsSurveyOwner]

    '''
    Create a submission only if the survey chosen by user is active.
    submission can be completed only if all questions are answered,
    so user cannot set is_complete = True during creation of submission
    '''

    def create(self, request, *args, **kwargs):
        serializer = SubmissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        survey = serializer.data['survey']
        # created = serializer.data['created_at']
        is_complete = serializer.data['is_complete']

        survey_chosen = Survey.objects.get(id=survey)

        with transaction.atomic():
            if not survey_chosen.creator:
                return Response('Submission cannot be created for template '
                                'survey')
            elif survey_chosen.creator.id == request.user.id:
                if survey_chosen.is_active:
                    if serializer.data['is_complete']:
                        return Response(
                            'Submission cannot be completed during creation, '
                            'Please uncheck is_complete')
                    else:
                        submission = Submission.objects.create(
                            survey_id=survey,
                            # created_at=created,
                            is_complete=is_complete,
                            submitter_id=request.user.id)

                        return Response(SubmissionSerializer(submission).data,
                                        status=201)
                else:
                    return Response(
                        'Survey is not active, cannot create submission')
            else:
                return Response('Submission cannot be created for other '
                                'users survey')

    def update(self, request, *args, **kwargs):
        choices = False
        text = False
        submission_survey = self.get_object()
        serializer = self.get_serializer(submission_survey, data=request.data)
        serializer.is_valid(raise_exception=True)
        answer_choice = AnswerChoice.objects.filter(
            submission_id=submission_survey.id)
        answer_text = AnswerText.objects.filter(
            submission_id=submission_survey.id)

        if answer_choice:
            for answer in range(len(answer_choice)):
                if answer_choice[answer].option_id is not None:
                    choices = True
                else:
                    choices = False
        else:
            choices = False
        if answer_text:
            for answer in range(len(answer_text)):
                if answer_text[answer].comment is not None:
                    text = True
                else:
                    text = False
        else:
            text = False

        if choices and text and serializer.validated_data['survey'].id == \
                submission_survey.survey_id:
            Submission.objects.filter(id=submission_survey.id).update(
                survey_id=serializer.validated_data['survey'],
                # created_at=serializer.validated_data['created_at'],
                is_complete=serializer.validated_data['is_complete'],
                submitter_id=request.user.baseuser.id)

            # ''' Generate report on submission of survey'''
            # if serializer.validated_data['is_complete']:
            #     self.generate_report()

            return Response('Survey updated')
        else:
            return Response(
                'Complete the survey to submit it / Invalid submission')

    # def generate_report(self):
    #     matplotlib.use('Agg')
    #     template_questions = Question.objects.filter(template_question=True)
    #     q1 = template_questions[0]
    #     q2 = template_questions[1]
    #     q3 = template_questions[2]
    #     x = np.array(q1, q2, q3)
    #     y = np.array([35, 25, 25, 15])
    #
    #     plt.pie(y)
    #     plt.savefig('chart2.png')
    #
    #     return 1

    def destroy(self, request, *args, **kwargs):
        submission_survey = self.get_object()
        if not submission_survey.is_complete:
            self.perform_destroy(submission_survey)
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.user and request.user.is_staff:
            self.perform_destroy(submission_survey)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('Only authorized user can delete completed '
                            'submission')

    def perform_destroy(self, survey_chosen):
        with transaction.atomic():
            survey_chosen.delete()


class AnswerChoiceAPIViewSet(ModelViewSet):
    queryset = AnswerChoice.objects.all()
    serializer_class = AnswerChoiceSerializer
    permission_classes = [IsAuthenticated, IsSubmissionOwner]

    '''
    Users will be able to answer only if the submission is created.
    Allow users to edit the answers only if the survey is active
    '''

    def create(self, request, *args, **kwargs):
        serializer = AnswerChoiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        submission = serializer.data['submission']
        question = serializer.data['question']
        option = serializer.data['option']

        survey_submission = Submission.objects.get(id=submission)
        survey_chosen = Survey.objects.get(id=survey_submission.survey_id)

        if survey_chosen.is_active and not survey_submission.is_complete:
            question_chosen = Question.objects.get(id=question)

            if question_chosen.type == 'cho':
                AnswerChoice.objects.create(submission_id=submission,
                                            question_id=question,
                                            option_id=option)
            else:
                return Response('Choose valid question')
            return Response(serializer.data, status=201)
        else:
            return Response('Survey is either not active or already submitted')

    '''
    Allow users to update only the answers to the added question,
    only if the survey is active and submission is not complete.
    Check if the user is unable to edit the submitted answers.
    '''

    def update(self, request, *args, **kwargs):
        answer_choice = self.get_object()
        serializer = self.get_serializer(answer_choice, data=request.data)
        serializer.is_valid(raise_exception=True)
        survey_submission = Submission.objects.get(
            id=answer_choice.submission_id)
        survey_chosen = Survey.objects.get(id=survey_submission.survey_id)
        if survey_chosen.is_active and not survey_submission.is_complete \
                and serializer.validated_data['submission'].id == \
                answer_choice.submission_id \
                and serializer.validated_data['question'].id == \
                answer_choice.question_id:
            AnswerChoice.objects.filter(id=answer_choice.id).update(
                submission_id=serializer.validated_data['submission'],
                question_id=serializer.validated_data['question'],
                option_id=serializer.validated_data['option']
                )
            serializer.save()
            return Response(serializer.data)
        else:
            return Response('Invalid update')


class AnswerTextAPIViewSet(ModelViewSet):
    queryset = AnswerText.objects.all()
    serializer_class = AnswerTextSerializer
    permission_classes = [IsAuthenticated, IsSubmissionOwner]

    '''
        Users will be able to answer only if the submission is created.
        Allow users to edit the answers only if the survey is active
    '''

    def create(self, request, *args, **kwargs):
        serializer = AnswerTextSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        submission = serializer.data['submission']
        question = serializer.data['question']
        comment = serializer.data['comment']

        survey_submission = Submission.objects.get(id=submission)

        survey_chosen = Survey.objects.get(id=survey_submission.survey_id)

        if survey_chosen.is_active and not survey_submission.is_complete:
            question_chosen = Question.objects.get(id=question)
            if question_chosen.type == 'txt':
                AnswerText.objects.create(submission_id=submission,
                                          question_id=question,
                                          comment=comment)
            else:
                return Response('Choose valid question')
            return Response(serializer.data, status=201)
        else:
            return Response('Survey is either not active or already submitted')

    '''
        Allow users to update only the answers to the added question,
        only if the survey is active and submission is not complete.
        Check if the user is unable to edit the submitted answers.
    '''

    def update(self, request, *args, **kwargs):
        answer_text = self.get_object()
        serializer = self.get_serializer(answer_text, data=request.data)
        serializer.is_valid(raise_exception=True)
        survey_submission = Submission.objects.get(
            id=answer_text.submission_id)

        survey_chosen = Survey.objects.get(id=survey_submission.survey_id)

        if survey_chosen.is_active and not survey_submission.is_complete \
                and serializer.validated_data['submission'].id == \
                answer_text.submission_id \
                and serializer.validated_data['question'].id == \
                answer_text.question_id:
            AnswerText.objects.filter(id=answer_text.id).update(
                submission_id=serializer.validated_data['submission'],
                question_id=serializer.validated_data['question'],
                comment=serializer.validated_data['comment']
                )
            serializer.save()
            return Response(serializer.data)
        else:
            return Response('Invalid update')
