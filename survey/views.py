from django.db import transaction
from django.http import Http404
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from baseuser.models import BaseUsers
from company.models import Company
from survey.models import Survey, Question, Option, Submission, AnswerChoice, AnswerText, SurveyQuestion
from survey.serializers import SurveySerializer, QuestionSerializer, OptionSerializer, SubmissionSerializer, \
    AnswerChoiceSerializer, AnswerTextSerializer, SurveyQuestionSerializer


class SurveyAPIViewSet(ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer

    def create(self, request, *args, **kwargs):
        serializer = SurveySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        title = serializer.data['title']
        is_active = serializer.data['is_active']
        creator = serializer.data['creator']
        company = serializer.data['company']
        created_at = serializer.data['created_at']

        with transaction.atomic():
            """Create Survey"""
            survey_creator = BaseUsers.objects.get(id=creator)
            survey_company = Company.objects.get(id=company)
            survey = Survey.objects.create(title=title, is_active=is_active, creator=survey_creator,
                                           company=survey_company, created_at=created_at)
            survey.save()

            """Template Question 1"""
            template_question_1 = Question.objects.create(prompt="Question 1", type='cho', template_question=True)
            template_question_1.save()
            template_question_1_option_1 = Option.objects.create(question=template_question_1, text="True")
            template_question_1_option_1.save()
            template_question_1_option_2 = Option.objects.create(question=template_question_1, text="False")
            template_question_1_option_2.save()
            # related to template question 1

            """Template Question 2"""
            template_question_2 = Question.objects.create(prompt="Question 2", type='cho', template_question=True)
            template_question_2.save()
            template_question_2_option_1 = Option.objects.create(question=template_question_2, text="Strongly Agree")
            template_question_2_option_1.save()
            template_question_2_option_2 = Option.objects.create(question=template_question_2, text="Agree")
            template_question_2_option_2.save()
            template_question_2_option_3 = Option.objects.create(question=template_question_2, text="Neutral")
            template_question_2_option_3.save()
            template_question_2_option_4 = Option.objects.create(question=template_question_2, text="Disagree")
            template_question_2_option_4.save()
            template_question_2_option_5 = Option.objects.create(question=template_question_2, text="Strongly Disagree")
            template_question_2_option_5.save()

            """Template Question 3"""
            template_question_3 = Question.objects.create(prompt="Question 3", type='txt', template_question=True)
            template_question_3.save()

            """Combine Template Questions with Company Survey"""
            survey_question_1 = SurveyQuestion.objects.create(survey=survey, question=template_question_1)
            survey_question_1.save()
            survey_question_2 = SurveyQuestion.objects.create(survey=survey, question=template_question_2)
            survey_question_2.save()
            survey_question_3 = SurveyQuestion.objects.create(survey=survey, question=template_question_3)
            survey_question_3.save()

            return Response(SurveySerializer(survey).data, status=201)

class QuestionAPIViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer



class SurveyQuestionAPIViewSet(ModelViewSet):
    queryset = SurveyQuestion.objects.all()
    serializer_class = SurveyQuestionSerializer

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
            SurveyQuestion.objects.create(survey_id=survey, question_id=question)
            return Response(serializer.data, status=201)


class OptionAPIViewSet(ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer


class SubmissionAPIViewSet(ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    '''
    Create a submission only if the survey chosen by user is active
    '''
    def create(self, request, *args, **kwargs):
        serializer = SubmissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        survey = serializer.data['survey']
        created = serializer.data['created_at']
        is_complete = serializer.data['is_complete']
        submitter = serializer.data['submitter']

        survey_chosen = Survey.objects.get(id=serializer.validated_data['survey'].id)
        if survey_chosen.is_active:
            Submission.objects.create(survey_id=survey, created_at=created, is_complete=is_complete,
                                      submitter_id=submitter)

            return Response(serializer.data, status=201)
        else:
            return Response('Survey is not active, cannot create submission')

class AnswerChoiceAPIViewSet(ModelViewSet):
    queryset = AnswerChoice.objects.all()
    serializer_class = AnswerChoiceSerializer

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

        if survey_chosen.is_active and survey_submission.is_complete == False:
            question_chosen = Question.objects.get(id=question)

            if question_chosen.type == 'cho':
                AnswerChoice.objects.create(submission_id=submission, question_id=question, option_id=option)
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
        print(answer_choice.id)
        serializer = self.get_serializer(answer_choice, data=request.data)
        serializer.is_valid(raise_exception=True)
        survey_submission = Submission.objects.get(id=answer_choice.submission_id)
        print(f'Is survey_submission complete - {survey_submission.is_complete}')
        survey_chosen = Survey.objects.get(id=survey_submission.survey_id)

        print(f'survey_chosen.is_active: {survey_chosen.is_active}')

        print(f"serializer.validated_data[submision]: {serializer.validated_data['submission'].id}")

        print(f"serializer.validated_data[question]: {serializer.validated_data['question'].id}")

        if survey_chosen.is_active and survey_submission.is_complete == False \
                and serializer.validated_data['submission'].id == answer_choice.submission_id\
                and serializer.validated_data['question'].id ==answer_choice.question_id:
            AnswerChoice.objects.filter(id=answer_choice.id).update(submission_id=serializer.validated_data['submission'],
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

        print(f'submission chosen :{submission}')

        survey_submission = Submission.objects.get(id=submission)
        print(f'Is survey_submission complete - {survey_submission.is_complete}')

        survey_chosen = Survey.objects.get(id=survey_submission.survey_id)
        print(f'survey chosen to answer: {survey_chosen.id} - {survey_chosen.is_active}')

        if survey_chosen.is_active and survey_submission.is_complete == False:
            question_chosen = Question.objects.get(id=question)
            if question_chosen.type == 'txt':
                AnswerText.objects.create(submission_id=submission, question_id=question, comment=comment)
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
        print(answer_text.id)
        serializer = self.get_serializer(answer_text, data=request.data)
        serializer.is_valid(raise_exception=True)
        survey_submission = Submission.objects.get(id=answer_text.submission_id)
        print(f'Is survey_submission complete - {survey_submission.is_complete}')
        survey_chosen = Survey.objects.get(id=survey_submission.survey_id)

        print(f'survey_chosen.is_active: {survey_chosen.is_active}')

        print(f"serializer.validated_data[submision]: {serializer.validated_data['submission'].id}")

        print(f"serializer.validated_data[question]: {serializer.validated_data['question'].id}")

        if survey_chosen.is_active and survey_submission.is_complete == False \
                and serializer.validated_data['submission'].id == answer_text.submission_id\
                and serializer.validated_data['question'].id ==answer_text.question_id:
            AnswerText.objects.filter(id=answer_text.id).update(submission_id=serializer.validated_data['submission'],
                                                                question_id=serializer.validated_data['question'],
                                                                comment=serializer.validated_data['comment']
                                                                )
            serializer.save()
            return Response(serializer.data)
        else:
            return Response('Invalid update')