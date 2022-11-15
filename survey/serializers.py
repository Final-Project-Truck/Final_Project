from rest_framework.serializers import ModelSerializer

from survey.models import Survey, Question, Option, Submission, AnswerChoice, AnswerText


class SurveySerializer(ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class OptionSerializer(ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'


class SubmissionSerializer(ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'


class AnswerChoiceSerializer(ModelSerializer):
    class Meta:
        model = AnswerChoice
        fields = '__all__'


class AnswerTextSerializer(ModelSerializer):
    class Meta:
        model = AnswerText
        fields = '__all__'
