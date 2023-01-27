from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from baseuser.models import BaseUsers, UserProfile, CompanyProfile


# class BaseUsersSafeSerializer(ModelSerializer):
#     class Meta:
#         model = BaseUsers
#         exclude = ['django_user', 'password']


class BaseUsersSerializer(ModelSerializer):
    class Meta:
        model = BaseUsers
        exclude = ['django_user']
        extra_kwargs = {'password': {'write_only': True}}


class UserProfileSerializer(ModelSerializer):

    class Meta:
        model = UserProfile
        fields = '__all__'


class CompanyProfileSerializer(ModelSerializer):

    class Meta:
        model = CompanyProfile
        fields = '__all__'


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = BaseUsers
        fields = ('password',)
