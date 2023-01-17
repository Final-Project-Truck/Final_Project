"""The_Truck_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from baseuser.views import BaseUsersAPIViewSet, BaseUsersSafeAPIViewSet, \
    UserProfileAPIViewSet, CompanyProfileAPIViewSet
from baseuser.views import registerPage, loginPage, logoutUser, home
from company.views import CompanyAPIViewSet
from company.views import JobPostingAPIViewSet
from survey.views import SurveyAPIViewSet, QuestionAPIViewSet, \
    OptionAPIViewSet, SubmissionAPIViewSet, \
    AnswerChoiceAPIViewSet, AnswerTextAPIViewSet
from survey.views import SurveyQuestionAPIViewSet

router = routers.DefaultRouter()
router.register(r'baseusers', BaseUsersAPIViewSet)
router.register(r'user-profile', UserProfileAPIViewSet)
router.register(r'company-profile', CompanyProfileAPIViewSet)
router.register(r'jobposting', JobPostingAPIViewSet)

router.register(r'companies', CompanyAPIViewSet)

router.register(r'survey', SurveyAPIViewSet)
router.register(r'questions', QuestionAPIViewSet)
router.register(r'survey_questions', SurveyQuestionAPIViewSet)
router.register(r'options', OptionAPIViewSet)
router.register(r'submissions', SubmissionAPIViewSet)
router.register(r'choice_answers', AnswerChoiceAPIViewSet)
router.register(r'text_answers', AnswerTextAPIViewSet)

urlpatterns = [
    path('', home, name="home"),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include(router.urls)),
    path('list_users/', BaseUsersSafeAPIViewSet.as_view()),
    path('admin/', admin.site.urls),
    path('register/', registerPage, name="register"),
    path('login/', loginPage, name="login"),
    path('logout/', logoutUser, name="logout"),
]
