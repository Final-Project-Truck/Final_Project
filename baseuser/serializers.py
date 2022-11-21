from rest_framework.serializers import ModelSerializer

from baseuser.models import BaseUsers


class BaseUsersSafeSerializer(ModelSerializer):
    class Meta:
        model = BaseUsers
        exclude = ['django_user', 'password']


class BaseUsersSerializer(ModelSerializer):
    class Meta:
        model = BaseUsers
        exclude = ['django_user']
        # extra_kwargs = {'password': {'write_only': True}}
