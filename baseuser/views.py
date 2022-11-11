from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from baseuser.models import BaseUsers
from baseuser.serializers import BaseUsersSerializer, BaseUsersSafeSerializer


class BaseUsersAPIViewSet(ModelViewSet):
    queryset = BaseUsers.objects.all()
    serializer_class = BaseUsersSerializer

    def create(self, request, *args, **kwargs):
        serializer = BaseUsersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data['username']
        password = serializer.data['password']
        email = serializer.data['email']

        with transaction.atomic():
            django_user = User.objects.create_user(username=username, password=password, email=email)
            base_user = BaseUsers.objects.create(**serializer.data, django_user=django_user)
            return Response(BaseUsersSerializer(base_user).data, status=201)


class BaseUsersSafeAPIViewSet(ListAPIView):
    queryset = BaseUsers.objects.all()
    serializer_class = BaseUsersSafeSerializer
