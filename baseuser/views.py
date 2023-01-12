from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import render, redirect
from rest_framework import status, generics, filters
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from baseuser.forms import CreateUserForm
from baseuser.models import BaseUsers, Profile, Search
from baseuser.serializers import BaseUsersSerializer, \
    BaseUsersSafeSerializer, SearchSerializer
from baseuser.serializers import ProfileSerializer


class BaseUsersAPIViewSet(ModelViewSet):
    queryset = BaseUsers.objects.all()
    serializer_class = BaseUsersSerializer

    def create(self, request, *args, **kwargs):
        serializer = BaseUsersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data['username']
        password1 = serializer.data['password1']
        password2 = serializer.data['password2']
        email = serializer.data['email']
        # Todo check password 'field level validation'
        with transaction.atomic():
            if password1 == password2:
                django_user = User.objects.create_user(username=username,
                                                       password=password2,
                                                       email=email)
                base_user = BaseUsers.objects.create(**serializer.data,
                                                     django_user=django_user)
                return Response(BaseUsersSerializer(base_user).data,
                                status=201)
            else:
                return Response('Error in password', status=400)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        baseuser = self.get_object()
        serializer = self.get_serializer(baseuser, data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            self.perform_update(serializer, baseuser)

        if getattr(baseuser, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            baseuser._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer, baseuser):
        with transaction.atomic():
            User.objects.filter(pk=baseuser.id).update(
                username=serializer.validated_data['username'],
                password=serializer.validated_data["password1"],
                email=serializer.validated_data["email"]
                )
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        baseuser = self.get_object()
        self.perform_destroy(baseuser)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, baseuser):
        with transaction.atomic():
            django_user = User.objects.filter(pk=baseuser.django_user_id)
            baseuser.delete()
            django_user.delete()


class BaseUsersSafeAPIViewSet(ListAPIView):
    queryset = BaseUsers.objects.all()
    serializer_class = BaseUsersSafeSerializer


def registerPage(request, django_user=None):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                with transaction.atomic():
                    user = form.save()
                    djangouser = User.objects.get(
                        email=form.cleaned_data['email'])
                    BaseUsers.objects.create(**form.cleaned_data,
                                             django_user_id=djangouser.id)
                messages.success(request,
                                 'Account was created for ' +
                                 djangouser.username)
                send_mail(
                    'Register Completed',  # Change your Subject
                    'Thank you for joining our Website',  # Change your message
                    'Final_Truck_Project@gmail.com',
                    # Put the email your going to use
                    [user.email],
                    fail_silently=False
                )
                return redirect('home')
        else:
            form = CreateUserForm()
        return render(request, 'register.html', {'form': form})


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
        return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def home(request):
    return render(request, 'home.html')


class ProfileUserAPIViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class SearchAPIView(generics.ListCreateAPIView):
    search_fields = ['key_word']
    filter_backends = (filters.SearchFilter,)
    queryset = Search.objects.all()
    serializer_class = SearchSerializer