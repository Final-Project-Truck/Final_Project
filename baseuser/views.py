from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status, filters, generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.models import Token

from baseuser.forms import BaseUsersForm
from baseuser.models import BaseUsers, UserProfile, CompanyProfile
from baseuser.serializers import BaseUsersSerializer, UserProfileSerializer, \
    CompanyProfileSerializer, ChangePasswordSerializer, \
    PersonBaseUsersSerializer, CompanyBaseUsersSerializer

'''
=============================API Views========================================
'''


class BaseUsersAPIViewSet(ModelViewSet):
    queryset = BaseUsers.objects.all()
    serializer_class = BaseUsersSerializer
    # permission_classes = (IsAuthenticated,)  # todo create a permission
    # clas is
    # Baseuser owner to replace the IsOwner and protect the retrieve view
    # todo not every authenticated shall be able to view the list of
    #  Baseusers??)
    # todo check the permissions
    # todo change the tests accordingly to check the permissions
    # @action(detail=False, methods=['post'])
    # def register(self, request):
    #     manager = UserManager()
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     data = serializer.validated_data
    #     try:
    #         user = manager.create_user(username=data['username'],
    #                                    email=data['email'],
    #                                    password=data['password'])
    #         base_user = BaseUsers.objects.create(username=data['username'],
    #                                              email=data['email'],
    #                                              django_user=user)
    #         headers = self.get_success_headers(serializer.data)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED,
    #                         headers=headers)
    #     except Exception as e:
    #         user.delete()
    #         return Response(str(e),
    #                         status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # And this the url of it
    # urlpatterns = [path('register/',
    # BaseUsersViewSet.as_view({'post': 'register'}), name='register'),]

    @action(detail=True, methods=['patch'])
    def change_password(self, request, pk=None):
        base_user = self.get_object()
        user = base_user.django_user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user.set_password(data['password'])
            user.save()
            return Response({'status': 'password set'},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    """"This change_password action is a patch method and it's only
    accessible for the single user, as specified by the detail=True
    argument. The get_object() method is used to retrieve the BaseUser
    object, and the set_password() method is used to set the new password
    for the related User object.
    Then, you can patch a request to the endpoint
    /baseusers/<pk>/change_password/
    with the new password in the payload and the request will change
    the password of both the BaseUser and the related User."""

    @action(methods=['post'], detail=False, permission_classes=[AllowAny])
    def register_person(self, request):  # todo since it is part of the
        # BaseUser viewset, then might be no way to hide the field person
        serializer = PersonBaseUsersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Person base user created successfully.'})

    @action(methods=['post'], detail=False, permission_classes=[AllowAny])
    def register_company(self, request):
        serializer = CompanyBaseUsersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Company base user created successfully.'})


class BaseUserRegisterAPIView(generics.CreateAPIView):
    pass  # todo check whether you do it on separate page or as action in the
    # BaseUsersViewSet


'''The ObtainAuthToken view uses a serializer to deserialize the user's
credentials (username and password) from the request data.The Serializer class
is a part of Django REST framework, it provides a way to validate input data
and to convert it to a Python data structure. To use it send a post request
as follows:
POST /authenticate/
Content-Type: application/json
{
    "username": "testuser",
    "password": "testpassword"
}
The response will be:
HTTP/1.1 200 OK
Content-Type: application/json
{
    "token": "a1b2c3d4e5f6g7h8i9j10",
    "user_id": 1,
    "username": "testuser"
}'''


class TokenAuthenticationAPIView(ObtainAuthToken):  # todo check it again and
    # check if you can create it in a different way

    def post(self, request, *args, **kwargs):
        """
        The self.serializer_class attribute is set to the default serializer
        class AuthTokenSerializer which is used to validate the user
        credentials. The AuthTokenSerializer is a built-in serializer class
        that is included with the REST framework. It takes in the username
        and password fields as input and validates them.
        """
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        '''
        Once the serializer is validated, the user object is retrieved by
        calling serializer.validated_data['user'].
        '''

        user = serializer.validated_data['user']
        '''Using the get_or_create function from the Token model to create a
        new token for the user. If a token already exists for the user,
        it just retrieves it.'''

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })


class ChangePasswordAPIView(generics.UpdateAPIView):
    # todo check if it needs
    # refactoring, check the todos at your local
    # todo can be changed to an action page

    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = BaseUsers
    permission_classes = (IsAuthenticated,)  # todo check if an authenticated

    # user can change the password of other with this logic

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get(
                    "old_password")):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            # update the password in the BaseUsers table
            base_user = BaseUsers.objects.get(django_user=self.object)
            base_user.password = serializer.data.get("new_password")
            # base_user.password2 = serializer.data.get("new_password")
            base_user.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetAPIView(ModelViewSet):
    pass  # todo this should be update view or can be changed to an action page


class UserProfileAPIViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def create(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_reference = BaseUsers.objects.get(
            id=serializer.validated_data['base_user'].id)

        if user_reference.user_type == 'com':
            return Response(
                'A Company cannot create a User Profile'
            )
        else:
            self.perform_create(serializer)
            return Response(serializer.data, status=201)


class CompanyProfileAPIViewSet(ModelViewSet):
    search_fields = ['organization_type', 'company__name', 'website']
    filter_backends = (filters.SearchFilter,)
    queryset = CompanyProfile.objects.all()
    serializer_class = CompanyProfileSerializer

    def create(self, request, *args, **kwargs):
        serializer = CompanyProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company = serializer.data['company']
        website = serializer.data['website']
        number_of_employees = serializer.data['number_of_employees']
        organization_type = serializer.data['organization_type']
        revenue = serializer.data['revenue']

        if request.user.baseuser.user_type == 'com':
            CompanyProfile.objects.create(
                base_user_id=request.user.baseuser.id, company_id=company,
                website=website,
                number_of_employees=number_of_employees,
                organization_type=organization_type,
                revenue=revenue)
            return Response(serializer.data, status=201)
        else:
            return Response('Only authorized user can create company profile')


'''
=============================Form Views========================================
'''


def home(request):  # todo move the home with its templates to the home app
    return render(request, 'home.html')


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = BaseUsersForm(request.POST or None)

        if request.method == 'POST':
            form = BaseUsersForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password1']
                user_type = form.cleaned_data['user_type']
                with transaction.atomic():
                    djangouser, created = User.objects.get_or_create(
                        username=username,
                        defaults={'email': email,
                                  'password': make_password(password)})

                    if created:
                        BaseUsers.objects.create(
                            username=username,
                            email=email,
                            password=password,
                            django_user=djangouser,
                            user_type=user_type)
                        messages.success(request,
                                         'Account was created for ' +
                                         djangouser.username)
                        send_mail(
                            'Register Completed',  # Change your Subject
                            'Thank you for joining our Website',
                            # Change your message
                            'struckproject@gmail.com',  # todo change this to
                            # a variable from the settings
                            # Put the email your going to use
                            [djangouser.email],
                            fail_silently=False
                        )
                        return redirect('home')
                    else:
                        messages.error(request, 'Username already taken')
        return render(request, 'registerPage.html', {'form': form})


def forget_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)  # todo this should be
            # changed to get by username since the user email is not unique
            if user.is_active:
                token = default_token_generator.make_token(user)
                x = reverse("password_reset_confirm",
                            kwargs={"token": token,
                                    "uidb64": urlsafe_base64_encode
                                    (force_bytes(user.pk))})
                email_body = f'Please click the link below to reset your ' \
                             f'password: \n' \
                             f'http://{request.get_host()}' \
                             f'{x}'
                send_mail(
                    'Password reset on your account',
                    email_body,
                    'struckproject@gmail.com',
                    [user.email],
                    fail_silently=False,
                )
                messages.success(request,
                                 f'An email has been sent to {email} to '
                                 f'reset your password.')
                return redirect('login')
            else:
                messages.error(request,
                               'Your account has been deactivated. Please '
                               'contact the administrator.')
                return redirect('forget_password')
        except User.DoesNotExist:
            messages.error(request, f'No account found with email {email}.')
            return redirect('forget_password')
    else:
        return render(request, 'forget_password.html')


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'loginPage.html', context)


def logoutPage(request):
    logout(request)
    return redirect('loginPage')
