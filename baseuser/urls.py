from django.contrib.auth import views as auth_views
from django.urls import path, include
from rest_framework import routers

from baseuser.views import BaseUsersAPIViewSet, UserProfileAPIViewSet, \
    CompanyProfileAPIViewSet  # , BaseUsersSafeAPIViewSet, \

# from baseuser.views import registerPage, loginPage, logoutPage, home


router = routers.DefaultRouter()
router.register(r'baseusers', BaseUsersAPIViewSet)
router.register(r'user-profile', UserProfileAPIViewSet)
router.register(r'company-profile', CompanyProfileAPIViewSet)


urlpatterns = [
    path('', include(router.urls),
         name='baseusers'),
    path('api-auth/', include('rest_framework.urls')),
    # path('list_users/', BaseUsersSafeAPIViewSet.as_view()),
    #   path('registerPage/', registerPage, name="registerPage"),
    #  path('loginPage/', loginPage, name="loginPage"),
    # path('logoutPage/', logoutPage, name="logoutPage"),
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

]
