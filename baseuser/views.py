from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status, filters, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from baseuser.forms import BaseUsersForm
from baseuser.models import BaseUsers, UserProfile, CompanyProfile
from baseuser.serializers import BaseUsersSerializer, UserProfileSerializer, \
    CompanyProfileSerializer, ChangePasswordSerializer


class BaseUsersAPIViewSet(ModelViewSet):
    queryset = BaseUsers.objects.all()
    serializer_class = BaseUsersSerializer


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
                        defaults={'email': email, 'password':
                            make_password(password)})
                    if created:
                        BaseUsers.objects.create(
                            username=username,
                            email=email,
                            password=password,
                            django_user=djangouser)


                        # django_user=
                        # djangouser.email = form.cleaned_data['email']
                        # djangouser.set_password(form.cleaned_data['password1'])
                        # djangouser.save()
                        # BaseUsers.objects.create(     # todo either change this to
                        #     # remove the unpacking data
                        #     # or you resolve it in the
                        #     # form **form.cleaned_data
                        #     username=form.cleaned_data['username'],
                        #     password=djangouser.password,
                        #     email=djangouser.email,
                        #     django_user=djangouser)

                        messages.success(request,
                                         'Account was created for ' +
                                         djangouser.username)
                        send_mail(
                            'Register Completed',  # Change your Subject
                            'Thank you for joining our Website',
                            # Change your message
                            'struckproject@gmail.com',  # todo change this to
                            # a varaible from the settings
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


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = BaseUsers
    permission_classes = (IsAuthenticated,)

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


def home(request):
    return render(request, 'home.html')


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
