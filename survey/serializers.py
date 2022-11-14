from rest_framework.serializers import ModelSerializer

from survey.models import Survey, SurveyQuestion, SurveyAnswer


class SurveySerializer(ModelSerializer):
    class Meta:
        model = Survey
        exclude = ['defunct_company', 'user']


class SurveyQuestionSerializer(ModelSerializer):
    class Meta:
        model = SurveyQuestion
        exclude = ['question_id']


class SurveyAnswerSerializer(ModelSerializer):
    class Meta:
        model = SurveyAnswer
        exclude = ['answer_id']
