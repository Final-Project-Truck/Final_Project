from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from baseuser.models import BaseUsers
from baseuser.serializers import BaseUsersSerializer, BaseUsersSafeSerializer
from baseuser.forms import CreateUserForm
from baseuser.models import BaseUsers


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

        with transaction.atomic():
            if password1 == password2: #Todo check password 'field level validation'
                django_user = User.objects.create_user(username=username, password=password2, email=email)
                base_user = BaseUsers.objects.create(**serializer.data, django_user=django_user)
                return Response(BaseUsersSerializer(base_user).data, status=201)
            else:
                return Response('Error in password', status=400)


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
                    form.save()
                    djangouser = User.objects.get(email=form.cleaned_data['email'])
                    BaseUsers.objects.create(**form.cleaned_data, django_user_id = djangouser.id)
                messages.success(request, 'Account was created for ' + djangouser.username)

                return redirect('login')

        context = {'form': form}

        return render(request, 'register.html', context)


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
