from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from survey.models import Survey, Question, Option, Submission, AnswerChoice, AnswerText
from survey.serializers import SurveySerializer, QuestionSerializer, OptionSerializer, SubmissionSerializer, \
    AnswerChoiceSerializer, AnswerTextSerializer


class SurveyAPIViewSet(ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer


class QuestionAPIViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


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
