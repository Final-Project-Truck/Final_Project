from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from baseuser.models import BaseUsers, UserProfile, CompanyProfile


class BaseUsersSafeSerializer(ModelSerializer):
    class Meta:
        model = BaseUsers
        exclude = ['django_user', 'password1', 'password2']


class BaseUsersSerializer(ModelSerializer):
    class Meta:
        model = BaseUsers
        exclude = ['django_user']
        # extra_kwargs = {'password': {'write_only': True}}


class UserProfileSerializer(ModelSerializer):


    class Meta:
        model = UserProfile
        fields = '__all__'


class CompanyProfileSerializer(ModelSerializer):

    class Meta:
        model = CompanyProfile
        fields = '__all__'
