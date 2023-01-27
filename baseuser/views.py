from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import transaction
from django.urls import reverse
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status, filters
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from baseuser.forms import BaseUsersForm
from baseuser.models import BaseUsers, UserProfile, CompanyProfile
from baseuser.serializers import BaseUsersSerializer, UserProfileSerializer, \
    CompanyProfileSerializer#, BaseUsersSafeSerializer


class BaseUsersAPIViewSet(ModelViewSet):
    queryset = BaseUsers.objects.all()
    serializer_class = BaseUsersSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = BaseUsersSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     username = serializer.data['username']
    #     password = serializer.data['password']
    #
    #     email = serializer.data['email']
    #     # Todo check password 'field level validation'
    #     with transaction.atomic():
    #
    #         django_user = User.objects.create_user(username=username,
    #                                                password=password,
    #                                                email=email)
    #         base_user = BaseUsers.objects.create(**serializer.data,
    #                                              django_user=django_user)
    #         return Response(BaseUsersSerializer(base_user).data,
    #                         status=201)
    #
    #
    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     baseuser = self.get_object()
    #     serializer = self.get_serializer(baseuser, data=request.data,
    #                                      partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     with transaction.atomic():
    #         self.perform_update(serializer, baseuser)
    #
    #     if getattr(baseuser, '_prefetched_objects_cache', None):
    #         # If 'prefetch_related' has been applied to a queryset, we need to
    #         # forcibly invalidate the prefetch cache on the instance.
    #         baseuser._prefetched_objects_cache = {}
    #
    #     return Response(serializer.data)
    #
    # def perform_update(self, serializer, baseuser):
    #     with transaction.atomic():
    #         User.objects.filter(pk=baseuser.id).update(
    #             username=serializer.validated_data['username'],
    #             password=serializer.validated_data["password"],
    #             email=serializer.validated_data["email"]
    #         )
    #     serializer.save()
    #
    # def partial_update(self, request, *args, **kwargs):
    #     kwargs['partial'] = True
    #     return self.update(request, *args, **kwargs)
    #
    # def destroy(self, request, *args, **kwargs):
    #     baseuser = self.get_object()
    #     self.perform_destroy(baseuser)
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    #
    # def perform_destroy(self, baseuser):
    #     with transaction.atomic():
    #         django_user = User.objects.filter(pk=baseuser.django_user_id)
    #         baseuser.delete()
    #         django_user.delete()


# class BaseUsersSafeAPIViewSet(ListAPIView):
#     queryset = BaseUsers.objects.all()
#     serializer_class = BaseUsersSafeSerializer


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = BaseUsersForm(request.POST or None)
        if request.method == 'POST':
            form = BaseUsersForm(request.POST)
            if form.is_valid():
                with transaction.atomic():
                    djangouser, created = User.objects.get_or_create(
                        username=form.cleaned_data['username'])
                    if created:
                        djangouser.email = form.cleaned_data['email']
                        djangouser.set_password(form.cleaned_data['password'])
                        djangouser.save()
                        BaseUsers.objects.create(**form.cleaned_data,
                                                 django_user=djangouser)
                        messages.success(request,
                                         'Account was created for ' +
                                         djangouser.username)
                        send_mail(
                            'Register Completed',  # Change your Subject
                            'Thank you for joining our Website',
                            # Change your message
                            'struckproject@gmail.com',
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
            user = User.objects.get(email=email)
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
        base_user = serializer.data['base_user']
        company = serializer.data['company']
        website = serializer.data['website']
        number_of_employees = serializer.data['number_of_employees']
        organization_type = serializer.data['organization_type']
        revenue = serializer.data['revenue']

        user_reference = BaseUsers.objects.get(
            id=serializer.validated_data['base_user'].id)

        if user_reference.user_type == 'per':
            return Response(
                'A Person cannot create a Company Profile'
            )
        else:
            CompanyProfile.objects.create(
                base_user_id=base_user, company_id=company,
                website=website,
                number_of_employees=number_of_employees,
                organization_type=organization_type,
                revenue=revenue)
            return Response(serializer.data, status=201)
