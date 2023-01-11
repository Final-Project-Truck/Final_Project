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
from django.contrib.auth import views as auth_views
from rest_framework import routers

from baseuser import views
from baseuser.views import BaseUsersAPIViewSet, BaseUsersSafeAPIViewSet, ProfileUserAPIViewSet
from baseuser.views import registerPage, loginPage, logoutUser, home
from company.views import CompanyAPIViewSet
from company.views import JobPostingAPIViewSet
from survey.views import SurveyAPIViewSet, QuestionAPIViewSet, OptionAPIViewSet, SubmissionAPIViewSet, \
    AnswerChoiceAPIViewSet, AnswerTextAPIViewSet
from survey.views import SurveyQuestionAPIViewSet

router = routers.DefaultRouter()
router.register(r'baseusers', BaseUsersAPIViewSet)
router.register(r'profile', ProfileUserAPIViewSet)
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
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'),name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),
]
