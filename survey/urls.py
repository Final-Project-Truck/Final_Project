from django.urls import include, path
from rest_framework import routers

from survey.views import SurveyAPIViewSet, QuestionAPIViewSet, \
    OptionAPIViewSet, SubmissionAPIViewSet, AnswerChoiceAPIViewSet, \
    AnswerTextAPIViewSet, SurveyQuestionAPIViewSet


router = routers.DefaultRouter()

router.register(r'survey', SurveyAPIViewSet)
router.register(r'questions', QuestionAPIViewSet)
router.register(r'survey_questions', SurveyQuestionAPIViewSet)
router.register(r'options', OptionAPIViewSet)
router.register(r'submissions', SubmissionAPIViewSet)
router.register(r'choice_answers', AnswerChoiceAPIViewSet)
router.register(r'text_answers', AnswerTextAPIViewSet)

urlpatterns = [
    path('', include(router.urls), name='survey'),
]
