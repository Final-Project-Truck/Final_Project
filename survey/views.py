from django.db import transaction
from django.http import Http404
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from survey.models import Survey, Question, Option, Submission, AnswerChoice, AnswerText, SurveyQuestion
from survey.serializers import SurveySerializer, QuestionSerializer, OptionSerializer, SubmissionSerializer, \
    AnswerChoiceSerializer, AnswerTextSerializer, SurveyQuestionSerializer


class SurveyAPIViewSet(ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = SurveySerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     title = serializer.data['title']
    #     created_at = serializer.data['created_at']
    #     company = serializer.data['company']
    #     creator = serializer.data['creator']
    #
    #     with transaction.atomic():


class QuestionAPIViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class SurveyQuestionAPIViewSet(ModelViewSet):
    queryset = SurveyQuestion.objects.all()
    serializer_class = SurveyQuestionSerializer


class OptionAPIViewSet(ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer


class SubmissionAPIViewSet(ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer


class AnswerChoiceAPIViewSet(ModelViewSet):
    queryset = AnswerChoice.objects.all()
    serializer_class = AnswerChoiceSerializer


class AnswerTextAPIViewSet(ModelViewSet):
    queryset = AnswerText.objects.all()
    serializer_class = AnswerTextSerializer
