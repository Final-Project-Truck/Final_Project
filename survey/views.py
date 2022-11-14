from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from survey.models import Survey, SurveyQuestion, SurveyAnswer
from survey.serializers import SurveySerializer, SurveyQuestionSerializer, SurveyAnswerSerializer


class SurveyAPIViewSet(ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer


class SurveyQuestionAPIViewSet(ModelViewSet):
    queryset = SurveyQuestion.objects.all()
    serializer_class = SurveyQuestionSerializer


class SurveyAnswerAPIViewSet(ModelViewSet):
    queryset = SurveyAnswer.objects.all()
    serializer_class = SurveyAnswerSerializer
