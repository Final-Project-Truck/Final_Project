from rest_framework.serializers import ModelSerializer

from survey.models import Survey, Question, Option, Submission, AnswerChoice, \
    AnswerText, SurveyQuestion


class OptionSerializer(ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'


class AnswerChoiceSerializer(ModelSerializer):
    # for i in range(len(options)):
    #     print(options[i])
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
        exclude = ['template_question']


class SurveySerializer(ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    # user_name = serializers.ReadOnlyField()
    class Meta:
        model = Survey
        fields = '__all__'


class SurveyQuestionSerializer(ModelSerializer):
    survey_question = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = SurveyQuestion
        fields = '__all__'


class SubmissionSerializer(ModelSerializer):
    # survey = SurveySerializer(many=True, read_only=True)
    choice_submission = AnswerChoiceSerializer(many=True, read_only=True)
    text_submission = AnswerTextSerializer(many=True, read_only=True)

    class Meta:
        model = Submission
        fields = '__all__'
