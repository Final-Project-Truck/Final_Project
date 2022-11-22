from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from survey.models import Survey, Question, Option, Submission, AnswerChoice, AnswerText


class OptionSerializer(ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'



class AnswerChoiceSerializer(ModelSerializer):


    class Meta:
        model = AnswerChoice
        fields = '__all__'


class AnswerTextSerializer(ModelSerializer):
    class Meta:
        model = AnswerText
        fields = '__all__'


class QuestionSerializer(ModelSerializer):
    question_options = OptionSerializer(many=True, read_only=True)
    # for i in range(len(options)):
    #     print(options[i])
    class Meta:
        model = Question
        fields = '__all__'


class SurveySerializer(ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    # user_name = serializers.ReadOnlyField()
    class Meta:
        model = Survey
        fields = ['questions', 'title', 'is_active', 'created_at', 'company', 'creator']


class SubmissionSerializer(ModelSerializer):
    # survey_submission = SurveySerializer(many=True, read_only=True)
    choice_submission = AnswerChoiceSerializer(many=True, read_only=True)
    text_submission = AnswerTextSerializer(many=True, read_only=True)

    class Meta:
        model = Submission
        fields = '__all__'
