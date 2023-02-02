from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from baseuser.views import BaseUsersAPIViewSet, \
    UserProfileAPIViewSet, CompanyProfileAPIViewSet, ChangePasswordAPIView, \
    LoginAPIView
from baseuser.views import registerPage, loginPage, logoutPage
from company.views import CompanyAPIViewSet, JobPostCommentAPIViewSet, \
    PostLikeAPIViewSet

from company.views import JobPostingAPIViewSet
from survey.views import SurveyAPIViewSet, QuestionAPIViewSet, \
    OptionAPIViewSet, SubmissionAPIViewSet, \
    AnswerChoiceAPIViewSet, AnswerTextAPIViewSet
from survey.views import SurveyQuestionAPIViewSet
from analytics.views import generate_report
from chat import views
from chat.views import MessageViewSet

from home.views import home_page, company_list, company_details, \
    SurveyCreationView, add_company, test_company, get_surveys_by_company

# from django.urls import re_path

# base_user_list = BaseUsersAPIViewSet.as_view({
#     'post': 'register_person',
# })
#
# base_user_list = BaseUsersAPIViewSet.as_view({
#     'post': 'register_company',
# })
# base_user_list = BaseUsersAPIViewSet.as_view({
#     'patch': 'change_password'
# })

schema_view = get_schema_view(
    openapi.Info(
        title="The_Truck_Project",
        default_version='v1',
        description="Make a Survey",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="theman198888@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = routers.DefaultRouter()
router.register(r'baseusers', BaseUsersAPIViewSet)
router.register(r'user-profile', UserProfileAPIViewSet)
router.register(r'company-profile', CompanyProfileAPIViewSet)
router.register(r'job_posting', JobPostingAPIViewSet)
router.register(r'job_post_comment', JobPostCommentAPIViewSet)
router.register(r'companies', CompanyAPIViewSet)
router.register(r'survey', SurveyAPIViewSet)
router.register(r'questions', QuestionAPIViewSet)
router.register(r'survey_questions', SurveyQuestionAPIViewSet)
router.register(r'options', OptionAPIViewSet)
router.register(r'submissions', SubmissionAPIViewSet)
router.register(r'choice_answers', AnswerChoiceAPIViewSet)
router.register(r'text_answers', AnswerTextAPIViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'post_likes', PostLikeAPIViewSet)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),

    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/token-auth/login', LoginAPIView.as_view(),
         name='token_authentication'),  # a more secure authentication method
    # than the basic auth, this endpoint will be connected to the login_page
    # on the frontend , the front end login sends a post request to this
    # endpoint to authenticate the user to CRUD the data from the back end

    path('api/v1/', include(router.urls), name="api"),
    # todo check which apraoch is more compatible with restfull api
    #  without the following re path , the default path for register and
    #  change password (as actions) will be # api/v1/baseuser/register_person
    #  api/v1/baseuser/<pk>/change_password
    # re_path(r'^register_person/$', base_user_list, name='register_person'),
    # re_path(r'^register_company/$', base_user_list, name='register_company'),
    # re_path(r'^(?P<pk>[0-9]+)/change_password/$', base_user_list,
    #         name='change_password'),

    path('admin/', admin.site.urls),
    path('registerPage/', registerPage, name="registerPage"),
    path('loginPage/', loginPage, name="loginPage"),
    path('logoutPage/', logoutPage, name="logoutPage"),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'),
         name='password_reset_complete'),
    path('api/v1/report/', generate_report, name='report'),
    path('chat/v1', views.chat_view, name='chats'),
    path('chat/v1/<int:sender>/<int:receiver>/', views.message_view,
         name='chat'),
    path('api/v1/messages/<int:sender>/<int:receiver>/', views.message_list,
         name='message-detail'),
    path('api/v1/messages/', views.message_list, name='message-list'),
    path('api/v1/change-password/', ChangePasswordAPIView.as_view(),
         name='change-password'),

    #   ----home views front end-------
    path('', home_page, name="home"),
    path('companies/', company_list, name="company_list"),
    path('companies/<int:company_id>/', company_details),
    path('companies/add_company/', add_company, name='add_company'),
    path('survey/create/', SurveyCreationView.as_view()),
    path('test_form/', test_company, name='test_form'),
    path('companies/<int:company_id>/surveys/', get_surveys_by_company,
         name='get_surveys_by_company'),

]
